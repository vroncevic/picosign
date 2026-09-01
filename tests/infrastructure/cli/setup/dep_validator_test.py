# -*- coding: UTF-8 -*-

'''
Module
    dep_validator_test.py
Info
    Unit tests for CLIBundleDependenciesValidator class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock

from ats_utilities.option.imanager import IOptionManager

from picosign.core.service.iservice import IService
from picosign.infrastructure.command.command import CommandBundle
from picosign.infrastructure.cli.setup.dep_validator import CLIBundleDependenciesValidator


class TestCLIBundleDependenciesValidator(TestCase):
    '''Unit tests for CLIBundleDependenciesValidator.'''

    def test_validate_success(self) -> None:
        '''Tests validate success.'''
        mock_service = Mock(spec=IService)
        mock_parser = Mock(spec=IOptionManager)
        mock_command = Mock(spec=CommandBundle)

        dependencies = {
            'service': mock_service,
            'parser': mock_parser,
            'commands': [mock_command]
        }
        CLIBundleDependenciesValidator.validate(dependencies)

    def test_validate_none(self) -> None:
        '''Tests validate None raises error.'''
        with self.assertRaises(Exception):
            CLIBundleDependenciesValidator.validate(None)  # type: ignore

    def test_validate_invalid_type(self) -> None:
        '''Tests validate invalid type raises error.'''
        with self.assertRaises(Exception):
            CLIBundleDependenciesValidator.validate("not_a_mapping")  # type: ignore

    def test_is_valid_success(self) -> None:
        '''Tests is_valid returns True for valid dependencies.'''
        mock_service = Mock(spec=IService)
        mock_parser = Mock(spec=IOptionManager)
        mock_command = Mock(spec=CommandBundle)

        dependencies = {
            'service': mock_service,
            'parser': mock_parser,
            'commands': [mock_command]
        }
        self.assertTrue(CLIBundleDependenciesValidator.is_valid(dependencies))

    def test_is_valid_failure(self) -> None:
        '''Tests is_valid returns False for invalid dependencies.'''
        self.assertFalse(CLIBundleDependenciesValidator.is_valid(None))  # type: ignore
        self.assertFalse(CLIBundleDependenciesValidator.is_valid("not_a_mapping"))  # type: ignore
        self.assertFalse(CLIBundleDependenciesValidator.is_valid({'service': 'invalid'}))  # type: ignore
