# -*- coding: UTF-8 -*-

'''
Module
    engine_test.py
Info
    Unit tests for CLI adapter.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock

from ats_utilities.option.imanager import IOptionManager
from ats_utilities.exceptions import ATSRuntimeError

from picosign.core.service.iservice import IService
from picosign.infrastructure.cli.engine import CLI
from picosign.infrastructure.cli.setup.bundle import CLIBundle
from picosign.infrastructure.command.command import CommandBundle
from picosign.infrastructure.command.sign_command_definition import SignCommandDefinition
from picosign.infrastructure.command.sign_command_executor import SignCommandExecutor


class TestCLI(TestCase):
    '''Unit tests for CLI adapter.'''

    def setUp(self) -> None:
        '''Sets up test bundle.'''
        self.mock_service = Mock(spec=IService)
        self.mock_parser = Mock(spec=IOptionManager)
        self.sign_def = SignCommandDefinition()
        self.sign_exec = SignCommandExecutor(definition=self.sign_def)
        self.sign_bundle = CommandBundle(definition=self.sign_def, executor=self.sign_exec)

        self.bundle = CLIBundle(
            service=self.mock_service,
            parser=self.mock_parser,
            commands=[self.sign_bundle]
        )

    def test_cli_init_and_run(self) -> None:
        '''Tests CLI initialization and running command.'''
        cli = CLI(bundle=self.bundle)
        self.assertTrue(cli.is_initialized())
        self.assertTrue(isinstance(str(cli), str))

        self.mock_parser.parse_command.return_value = ('sign', {'file': 'test.uf2'})
        self.mock_service.is_initialized.return_value = True
        self.mock_service.execute.return_value = {'returncode': 0, 'stdout': 'ok', 'stderr': ''}

        result = cli.run()
        self.assertEqual(result['returncode'], 0)

    def test_cli_command_not_found(self) -> None:
        '''Tests CLI when command is not recognized.'''
        cli = CLI(bundle=self.bundle)
        self.mock_parser.parse_command.return_value = ('unknown', {})
        result = cli.run()
        self.assertEqual(result['returncode'], 1)
        self.assertIn('command not found', str(result['stderr']))

    def test_cli_run_exception(self) -> None:
        '''Tests CLI handling exception during execution.'''
        cli = CLI(bundle=self.bundle)
        self.mock_parser.parse_command.side_effect = ATSRuntimeError('Parser crash')
        result = cli.run()
        self.assertEqual(result['returncode'], 1)
        self.assertIn('Parser crash', str(result['stderr']))
