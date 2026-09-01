# -*- coding: UTF-8 -*-

'''
Module
    subprocessor.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    picosign is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    picosign is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines subprocessor adapter implementing ISubProcessor for UF2 operations.
'''

from __future__ import annotations

from collections.abc import Mapping
from logging import INFO, ERROR
from os.path import isfile
from struct import unpack
from typing import ClassVar, override

from ats_utilities.logger.ilogger import ILogger
from ats_utilities.validation.check_value import not_none
from ats_utilities.validation.check_type import istype
from ats_utilities.utils.reflection import to_str

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/picosign'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/picosign/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SubProcessor:
    '''
        Adapter that executes UF2 signature read and write operations.

        It defines:

            :attributes:
                | UF2_MAGIC_START0 - UF2 header first magic number (0x0A324655).
                | UF2_MAGIC_START1 - UF2 header second magic number (0x9E5D5157).
                | UF2_MAGIC_END - UF2 block end magic number (0x0AB16F30).
                | CUSTOM_MARKER_HEADER - Signature marker prefix (b'SIG!').
                | BLOCK_SIZE - Standard UF2 block size (512 bytes).
                | PADDING_START - Offset where padding starts in block (288).
                | PADDING_END - Offset where padding ends in block (508).
                | MAX_SIG_LEN - Maximum signature length in bytes (220).
                | _logger - Logger used to log operational messages.
            :methods:
                | __init__ - Initializes the SubProcessor adapter.
                | run - Executes a UF2 signature sub-process.
                | is_initialized - Checks if the subprocessor is initialized.
                | __str__ - Returns the SubProcessor as string representation.
    '''

    UF2_MAGIC_START0: ClassVar[int] = 0x0A324655
    UF2_MAGIC_START1: ClassVar[int] = 0x9E5D5157
    UF2_MAGIC_END: ClassVar[int] = 0x0AB16F30
    CUSTOM_MARKER_HEADER: ClassVar[bytes] = b'SIG!'
    BLOCK_SIZE: ClassVar[int] = 512
    PADDING_START: ClassVar[int] = 288
    PADDING_END: ClassVar[int] = 508
    MAX_SIG_LEN: ClassVar[int] = 220

    _logger: ILogger

    def __init__(self, logger: ILogger) -> None:
        '''
            Initializes the SubProcessor adapter.

            :param logger: The logger instance.
            :exceptions:
                | ATSValueError: The logger must be provided.
                | ATSTypeError:  The logger must be an instance of ILogger.
        '''
        ctx: str = 'subprocessor::init(...)'
        msg_logger_none: str = 'the logger must be provided'
        msg_logger_istype: str = f'the logger must be an instance of {ILogger.__name__}'

        not_none(logger, ctx, msg_logger_none)
        istype(logger, ILogger, ctx, msg_logger_istype)

        self._logger = logger

    def _add_signature(self, input_file: str, output_file: str | None, signature_text: str) -> tuple[bool, str, str]:
        '''
            Embeds textual signature into the padding of the first UF2 block.

            :param input_file: Path to the input UF2 file.
            :param output_file: Path to the output UF2 file (or None for in-place).
            :param signature_text: Signature string to embed.
            :return: Tuple of (success flag, stdout message, stderr message).
        '''
        if not isfile(input_file):
            return False, '', f'file does not exist: {input_file}'

        try:
            with open(input_file, 'rb') as file_handle:
                data: bytearray = bytearray(file_handle.read())

            if len(data) == 0 or len(data) % self.BLOCK_SIZE != 0:
                return False, '', f'invalid UF2 file size ({len(data)} bytes, must be divisible by {self.BLOCK_SIZE})'

            magic0, magic1 = unpack('<II', data[0:8])
            if magic0 != self.UF2_MAGIC_START0 or magic1 != self.UF2_MAGIC_START1:
                return False, '', 'invalid UF2 magic header'

            sig_bytes: bytes = self.CUSTOM_MARKER_HEADER + signature_text.encode('utf-8')
            if len(sig_bytes) > self.MAX_SIG_LEN:
                return False, '', f'signature exceeds max allowed length ({len(sig_bytes)} > {self.MAX_SIG_LEN} bytes)'

            data[self.PADDING_START : self.PADDING_START + len(sig_bytes)] = sig_bytes
            target_out: str = output_file if output_file is not None else input_file

            with open(target_out, 'wb') as file_handle:
                file_handle.write(data)

            msg: str = f"Successfully wrote signature to '{target_out}'"
            self._logger.write_log(INFO, f'    {msg}')
            return True, msg, ''

        except OSError as exc:
            return False, '', f'failed to write signature: {exc}'

    def _read_signature(self, uf2_file: str) -> tuple[bool, str, str]:
        '''
            Reads and verifies signature from the first UF2 block.

            :param uf2_file: Path to the UF2 file.
            :return: Tuple of (success flag, stdout message, stderr message).
        '''
        if not isfile(uf2_file):
            return False, '', f'file does not exist: {uf2_file}'

        try:
            with open(uf2_file, 'rb') as file_handle:
                data: bytes = file_handle.read(self.BLOCK_SIZE)

            if len(data) < self.BLOCK_SIZE:
                return False, '', f'invalid UF2 file size (read {len(data)} bytes, expected at least {self.BLOCK_SIZE})'

            magic0, magic1 = unpack('<II', data[0:8])
            if magic0 != self.UF2_MAGIC_START0 or magic1 != self.UF2_MAGIC_START1:
                return False, '', 'invalid UF2 magic header'

            padding_data: bytes = data[self.PADDING_START:self.PADDING_END]
            if padding_data.startswith(self.CUSTOM_MARKER_HEADER):
                raw_sig: bytes = padding_data[len(self.CUSTOM_MARKER_HEADER):]
                clean_sig: str = raw_sig.split(b'\x00')[0].decode('utf-8', errors='ignore')
                msg: str = f"Found signature: '{clean_sig}'"
                self._logger.write_log(INFO, f'    {msg}')
                return True, msg, ''

            msg = 'Signature not found in UF2 file'
            self._logger.write_log(INFO, f'    {msg}')
            return True, msg, ''

        except OSError as exc:
            return False, '', f'failed to read signature: {exc}'

    @override
    def run(self, *, params: Mapping[str, object]) -> Mapping[str, object]:
        '''
            Executes the UF2 sub-process based on the action/command parameters.

            :param params: The command parameters mapping.
            :return: Return code, stdout and stderr messages.
            :exceptions: None.
        '''
        try:
            action: object = params.get('action')
            file_path: str = str(params.get('file', ''))
            output_path: str | None = str(params.get('output')) if params.get('output') else None
            sig_text: str = str(params.get('signature', 'AUTHOR: Vladimir Roncevic | BUILD: 2026-09-01 | VERSION: 1.0.0'))

            success: bool
            stdout_msg: str
            stderr_msg: str

            if action == 'read':
                success, stdout_msg, stderr_msg = self._read_signature(file_path)
            else:
                success, stdout_msg, stderr_msg = self._add_signature(file_path, output_path, sig_text)

            return {
                'returncode': 0 if success else 1,
                'stdout': stdout_msg,
                'stderr': stderr_msg
            }

        except Exception as exc:
            self._logger.write_log(ERROR, f'subprocessor execution error: {exc}')
            return {'returncode': 1, 'stdout': '', 'stderr': f'subprocessor error: {exc}'}

    @override
    def is_initialized(self) -> bool:
        '''
            Checks if the subprocessor is initialized.

            :return: True if the subprocessor is initialized, False otherwise.
            :exceptions: None.
        '''
        return self._logger is not None and self._logger.is_initialized()

    @override
    def __str__(self) -> str:
        '''
            Returns the SubProcessor as string representation.

            :return: The SubProcessor as string representation.
            :exceptions: None.
        '''
        return to_str(self)
