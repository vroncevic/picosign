# -*- coding: UTF-8 -*-

'''
Module
    read_command_test.py
Info
    Unit tests for ReadCommandDefinition and ReadCommandExecutor.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock

from picosign.core.service.iservice import IService
from picosign.infrastructure.command.read_command_definition import ReadCommandDefinition
from picosign.infrastructure.command.read_command_executor import ReadCommandExecutor


class TestReadCommand(TestCase):
    '''Unit tests for Read command definition and executor.'''

    def test_read_command_definition(self) -> None:
        '''Tests ReadCommandDefinition properties.'''
        cmd_def = ReadCommandDefinition()
        self.assertEqual(cmd_def.name, 'read')
        self.assertIn('Read signature', cmd_def.help_text)
        self.assertEqual(len(cmd_def.options), 1)
        self.assertTrue(isinstance(str(cmd_def), str))

    def test_read_command_executor(self) -> None:
        '''Tests ReadCommandExecutor execution.'''
        cmd_def = ReadCommandDefinition()
        executor = ReadCommandExecutor(definition=cmd_def)
        self.assertEqual(executor.get_definition(), cmd_def)
        self.assertTrue(isinstance(str(executor), str))

        mock_service = Mock(spec=IService)
        mock_service.is_initialized.return_value = True
        mock_service.execute.return_value = {'returncode': 0, 'stdout': 'found', 'stderr': ''}

        params = {'file': 'test.uf2'}
        result = executor.execute(params=params, service=mock_service)
        self.assertEqual(result['returncode'], 0)
        mock_service.execute.assert_called_once_with(params={'file': 'test.uf2', 'action': 'read'})

    def test_read_command_executor_uninitialized_service(self) -> None:
        '''Tests ReadCommandExecutor with uninitialized service.'''
        cmd_def = ReadCommandDefinition()
        executor = ReadCommandExecutor(definition=cmd_def)
        mock_service = Mock(spec=IService)
        mock_service.is_initialized.return_value = False

        result = executor.execute(params={'file': 'test.uf2'}, service=mock_service)
        self.assertEqual(result['returncode'], 1)
        self.assertIn('service not initialized', str(result['stderr']))
