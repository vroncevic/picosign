# -*- coding: UTF-8 -*-

'''
Module
    opt_validator_test.py
Info
    Unit tests for CLIBundleOptionsValidator class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock

from ats_utilities.option.imanager import IOptionManager

from picosign.core.service.iservice import IService
from picosign.infrastructure.cli.setup.opt_validator import CLIBundleOptionsValidator


class TestCLIBundleOptionsValidator(TestCase):
    '''Unit tests for CLIBundleOptionsValidator.'''

    def test_validate_success(self) -> None:
        '''Tests validation pass.'''
        mock_service = Mock(spec=IService)
        mock_parser = Mock(spec=IOptionManager)
        options = {'service': mock_service, 'parser': mock_parser}
        CLIBundleOptionsValidator.validate(options)

    def test_validate_none(self) -> None:
        '''Tests validate None raises error.'''
        with self.assertRaises(Exception):
            CLIBundleOptionsValidator.validate(None)  # type: ignore

    def test_validate_invalid_type(self) -> None:
        '''Tests validate invalid type raises error.'''
        with self.assertRaises(Exception):
            CLIBundleOptionsValidator.validate("not_a_mapping")  # type: ignore

    def test_is_valid_success(self) -> None:
        '''Tests is_valid returns True for valid options.'''
        mock_service = Mock(spec=IService)
        mock_parser = Mock(spec=IOptionManager)
        options = {'service': mock_service, 'parser': mock_parser}
        self.assertTrue(CLIBundleOptionsValidator.is_valid(options))

    def test_is_valid_failure(self) -> None:
        '''Tests is_valid returns False for invalid options.'''
        self.assertFalse(CLIBundleOptionsValidator.is_valid(None))  # type: ignore
        self.assertFalse(CLIBundleOptionsValidator.is_valid("not_a_mapping"))  # type: ignore
        self.assertFalse(CLIBundleOptionsValidator.is_valid({'service': 'invalid'}))  # type: ignore
