# -*- coding: UTF-8 -*-

'''
Module
    validator_test.py
Info
    Unit tests for CLIBundleValidator class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock

from ats_utilities.option.imanager import IOptionManager

from picosign.core.service.iservice import IService
from picosign.infrastructure.command.command import CommandBundle
from picosign.infrastructure.cli.setup.bundle import CLIBundle
from picosign.infrastructure.cli.setup.validator import CLIBundleValidator


class TestCLIBundleValidator(TestCase):
    '''Unit tests for CLIBundleValidator.'''

    def test_validate_success(self) -> None:
        '''Tests validate success.'''
        mock_service = Mock(spec=IService)
        mock_parser = Mock(spec=IOptionManager)
        mock_command = Mock(spec=CommandBundle)

        bundle = CLIBundle(
            service=mock_service,
            parser=mock_parser,
            commands=[mock_command]
        )
        CLIBundleValidator.validate(bundle)
        self.assertTrue(CLIBundleValidator.is_valid(bundle))

    def test_validate_failure(self) -> None:
        '''Tests validate failure.'''
        with self.assertRaises(Exception):
            CLIBundleValidator.validate(None)  # type: ignore

        self.assertFalse(CLIBundleValidator.is_valid(None))  # type: ignore
