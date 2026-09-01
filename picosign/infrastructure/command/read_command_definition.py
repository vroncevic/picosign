# -*- coding: UTF-8 -*-

'''
Module
    read_command_definition.py
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
    Defines ReadCommandDefinition class.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import override

from ats_utilities.option.command.data import OptionData
from ats_utilities.utils.reflection import to_str

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/picosign'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/picosign/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReadCommandDefinition:
    '''
        CLI subcommand metadata definition for reading signature from UF2 file.

        It defines:

            :methods:
                | name - Returns the command name.
                | help_text - Returns the command help text.
                | options - Returns the sequence of command options.
                | __str__ - Returns the command definition as string representation.
    '''

    @property
    def name(self) -> str:
        '''
            Returns the command name.

            :return: The command name.
        '''
        return 'read'

    @property
    def help_text(self) -> str:
        '''
            Returns the command help text.

            :return: The command help text.
        '''
        return 'Read signature from UF2 file'

    @property
    def options(self) -> Sequence[OptionData]:
        '''
            Returns the command options.

            :return: Sequence of command options.
        '''
        return [
            OptionData(
                name='--file',
                help_text='Path to the UF2 file',
                action=None,
                default=None,
                required=True,
                choices=None,
                nargs=None
            )
        ]

    @override
    def __str__(self) -> str:
        '''
            Returns the command definition as string representation.

            :return: The command definition as string representation.
        '''
        return to_str(self)
