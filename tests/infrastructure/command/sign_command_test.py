# -*- coding: UTF-8 -*-

'''
Module
    sign_command_test.py
Info
    Unit tests for SignCommandDefinition and SignCommandExecutor.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock

from picosign.core.service.iservice import IService
from picosign.infrastructure.command.sign_command_definition import SignCommandDefinition
from picosign.infrastructure.command.sign_command_executor import SignCommandExecutor


class TestSignCommand(TestCase):
    '''Unit tests for Sign command definition and executor.'''

    def test_sign_command_definition(self) -> None:
        '''Tests SignCommandDefinition properties.'''
        cmd_def = SignCommandDefinition()
        self.assertEqual(cmd_def.name, 'sign')
        self.assertIn('Add signature', cmd_def.help_text)
        self.assertEqual(len(cmd_def.options), 3)
        self.assertTrue(isinstance(str(cmd_def), str))

    def test_sign_command_executor(self) -> None:
        '''Tests SignCommandExecutor execution.'''
        cmd_def = SignCommandDefinition()
        executor = SignCommandExecutor(definition=cmd_def)
        self.assertEqual(executor.get_definition(), cmd_def)
        self.assertTrue(isinstance(str(executor), str))

        mock_service = Mock(spec=IService)
        mock_service.is_initialized.return_value = True
        mock_service.execute.return_value = {'returncode': 0, 'stdout': 'ok', 'stderr': ''}

        params = {'file': 'test.uf2', 'signature': 'sig'}
        result = executor.execute(params=params, service=mock_service)
        self.assertEqual(result['returncode'], 0)
        mock_service.execute.assert_called_once_with(params={'file': 'test.uf2', 'signature': 'sig', 'action': 'sign'})

    def test_sign_command_executor_uninitialized_service(self) -> None:
        '''Tests SignCommandExecutor with uninitialized service.'''
        cmd_def = SignCommandDefinition()
        executor = SignCommandExecutor(definition=cmd_def)
        mock_service = Mock(spec=IService)
        mock_service.is_initialized.return_value = False

        result = executor.execute(params={'file': 'test.uf2'}, service=mock_service)
        self.assertEqual(result['returncode'], 1)
        self.assertIn('service not initialized', str(result['stderr']))
