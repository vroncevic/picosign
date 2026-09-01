# -*- coding: UTF-8 -*-

'''
Module
    subprocessor_test.py
Info
    Unit tests for SubProcessor adapter.
'''

from __future__ import annotations

from os import remove
from os.path import exists
from struct import pack
from tempfile import NamedTemporaryFile
from unittest import TestCase
from unittest.mock import patch

from ats_utilities.logger.ilogger import ILogger

from picosign.infrastructure.subprocessor import SubProcessor


class DummyLogger(ILogger):
    '''Dummy logger for testing.'''

    def get_bundle(self) -> object:
        '''Gets logger configuration bundle.'''
        return None

    def is_initialized(self) -> bool:
        '''Checks if logger initialized.'''
        return True

    def update_bundle(self, bundle: object) -> bool:
        '''Updates logger bundle.'''
        return True

    def set_level(self, level: object) -> None:
        '''Sets log level.'''

    def set_log_file(self, log_file: object) -> bool:
        '''Sets log file.'''
        return True

    def set_stdout(self) -> bool:
        '''Sets stdout output.'''
        return True

    def stop_buffering(self) -> None:
        '''Stops log buffering.'''

    def write_log(self, level: object, message: object) -> None:
        '''Writes log message.'''

    def __str__(self) -> str:
        '''Returns string representation.'''
        return 'DummyLogger'


class TestSubProcessor(TestCase):
    '''Unit tests for SubProcessor.'''

    def setUp(self) -> None:
        '''Creates valid temporary UF2 block.'''
        self.logger = DummyLogger()
        self.subprocessor = SubProcessor(logger=self.logger)

        self.temp_file = NamedTemporaryFile(delete=False)
        # Create 512-byte valid UF2 block
        header = pack('<II', SubProcessor.UF2_MAGIC_START0, SubProcessor.UF2_MAGIC_START1)
        body = b'\x00' * (512 - 8 - 4)
        tail = pack('<I', SubProcessor.UF2_MAGIC_END)
        self.temp_file.write(header + body + tail)
        self.temp_file.close()

    def tearDown(self) -> None:
        '''Cleans up temporary files.'''
        if exists(self.temp_file.name):
            remove(self.temp_file.name)

    def test_init_errors(self) -> None:
        '''Tests init validation errors.'''
        with self.assertRaises(Exception):
            SubProcessor(logger=None)  # type: ignore
        with self.assertRaises(Exception):
            SubProcessor(logger='invalid')  # type: ignore

    def test_sign_and_read_success(self) -> None:
        '''Tests signing UF2 file and reading back signature.'''
        sig = 'AUTHOR: Test | VERSION: 1.0.0'
        out_file = NamedTemporaryFile(delete=False)
        out_file.close()
        try:
            res_sign = self.subprocessor.run(params={'action': 'sign', 'file': self.temp_file.name, 'output': out_file.name, 'signature': sig})
            self.assertEqual(res_sign['returncode'], 0)
            self.assertIn('Successfully wrote signature', str(res_sign['stdout']))

            res_read = self.subprocessor.run(params={'action': 'read', 'file': out_file.name})
            self.assertEqual(res_read['returncode'], 0)
            self.assertIn(sig, str(res_read['stdout']))
        finally:
            if exists(out_file.name):
                remove(out_file.name)

    def test_read_unsigned_file(self) -> None:
        '''Tests reading from unsigned UF2 file.'''
        res_read = self.subprocessor.run(params={'action': 'read', 'file': self.temp_file.name})
        self.assertEqual(res_read['returncode'], 0)
        self.assertIn('Signature not found', str(res_read['stdout']))

    def test_nonexistent_file(self) -> None:
        '''Tests operations on nonexistent file.'''
        res = self.subprocessor.run(params={'action': 'read', 'file': '/tmp/nonexistent.uf2'})
        self.assertEqual(res['returncode'], 1)
        self.assertIn('does not exist', str(res['stderr']))

        res_sign = self.subprocessor.run(params={'action': 'sign', 'file': '/tmp/nonexistent.uf2'})
        self.assertEqual(res_sign['returncode'], 1)
        self.assertIn('does not exist', str(res_sign['stderr']))

    def test_empty_file_and_invalid_size(self) -> None:
        '''Tests empty file and invalid size not divisible by 512.'''
        empty_file = NamedTemporaryFile(delete=False)
        empty_file.close()
        try:
            res = self.subprocessor.run(params={'action': 'sign', 'file': empty_file.name})
            self.assertEqual(res['returncode'], 1)
            self.assertIn('invalid UF2 file size', str(res['stderr']))

            res_read = self.subprocessor.run(params={'action': 'read', 'file': empty_file.name})
            self.assertEqual(res_read['returncode'], 1)
            self.assertIn('invalid UF2 file size', str(res_read['stderr']))
        finally:
            remove(empty_file.name)

    def test_invalid_magic_header(self) -> None:
        '''Tests file with invalid magic numbers.'''
        bad_file = NamedTemporaryFile(delete=False)
        bad_file.write(b'\x00' * 512)
        bad_file.close()
        try:
            res = self.subprocessor.run(params={'action': 'sign', 'file': bad_file.name})
            self.assertEqual(res['returncode'], 1)
            self.assertIn('invalid UF2 magic header', str(res['stderr']))

            res_read = self.subprocessor.run(params={'action': 'read', 'file': bad_file.name})
            self.assertEqual(res_read['returncode'], 1)
            self.assertIn('invalid UF2 magic header', str(res_read['stderr']))
        finally:
            remove(bad_file.name)

    def test_signature_too_long(self) -> None:
        '''Tests signature exceeding max length.'''
        long_sig = 'X' * 300
        res = self.subprocessor.run(params={'action': 'sign', 'file': self.temp_file.name, 'signature': long_sig})
        self.assertEqual(res['returncode'], 1)
        self.assertIn('exceeds max allowed length', str(res['stderr']))

    @patch('builtins.open', side_effect=OSError('Disk error'))
    def test_os_error_handling(self, mock_open: object) -> None:
        '''Tests OSError handling during file operations.'''
        res_sign = self.subprocessor.run(params={'action': 'sign', 'file': self.temp_file.name})
        self.assertEqual(res_sign['returncode'], 1)
        self.assertIn('failed to write signature', str(res_sign['stderr']))

        res_read = self.subprocessor.run(params={'action': 'read', 'file': self.temp_file.name})
        self.assertEqual(res_read['returncode'], 1)
        self.assertIn('failed to read signature', str(res_read['stderr']))

    def test_run_unexpected_exception(self) -> None:
        '''Tests unexpected exception inside run.'''
        with patch.object(self.subprocessor, '_read_signature', side_effect=RuntimeError('Unexpected failure')):
            res = self.subprocessor.run(params={'action': 'read', 'file': self.temp_file.name})
            self.assertEqual(res['returncode'], 1)
            self.assertIn('subprocessor error', str(res['stderr']))

    def test_str_representation(self) -> None:
        '''Tests string representation.'''
        self.assertTrue(isinstance(str(self.subprocessor), str))
