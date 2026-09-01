# -*- coding: UTF-8 -*-

'''
Module
    dep_validator_test.py
Info
    Unit tests for PicoSignBundleDependenciesValidator class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock

from ats_utilities.base.setup.bundle import BaseBundle

from picosign.setup.dep_validator import PicoSignBundleDependenciesValidator


class DummyService:
    '''Dummy service for testing.'''

    def execute(self, *, params: object) -> object:
        '''Executes service.'''
        return None

    def is_initialized(self) -> bool:
        '''Checks initialized.'''
        return True


class DummySubProcessor:
    '''Dummy subprocessor for testing.'''

    def run(self, *, params: object) -> dict[str, object]:
        '''Runs subprocessor.'''
        return {}

    def is_initialized(self) -> bool:
        '''Checks initialized.'''
        return True


class DummyCLI:
    '''Dummy CLI for testing.'''

    def run(self) -> dict[str, object]:
        '''Runs CLI.'''
        return {}

    def is_initialized(self) -> bool:
        '''Checks initialized.'''
        return True


class TestPicoSignBundleDependenciesValidator(TestCase):
    '''Unit tests for PicoSignBundleDependenciesValidator.'''

    def test_validate_success(self) -> None:
        '''Tests validation success.'''
        mock_base = Mock(spec=BaseBundle)
        dummy_service = DummyService()
        dummy_subprocessor = DummySubProcessor()
        dummy_cli = DummyCLI()

        dependencies = {
            'base': mock_base,
            'service': dummy_service,
            'subprocessor': dummy_subprocessor,
            'cli': dummy_cli
        }
        PicoSignBundleDependenciesValidator.validate(dependencies)

    def test_validate_none(self) -> None:
        '''Tests validate None raises error.'''
        with self.assertRaises(Exception):
            PicoSignBundleDependenciesValidator.validate(None)  # type: ignore

    def test_validate_invalid_type(self) -> None:
        '''Tests validate invalid type raises error.'''
        with self.assertRaises(Exception):
            PicoSignBundleDependenciesValidator.validate("not_a_mapping")  # type: ignore

    def test_validate_missing_dependency(self) -> None:
        '''Tests validate missing dependency raises error.'''
        mock_base = Mock(spec=BaseBundle)
        dummy_service = DummyService()
        dummy_subprocessor = DummySubProcessor()

        dependencies = {
            'base': mock_base,
            'service': dummy_service,
            'subprocessor': dummy_subprocessor
        }
        with self.assertRaises(Exception):
            PicoSignBundleDependenciesValidator.validate(dependencies)

    def test_is_valid_success(self) -> None:
        '''Tests is_valid returns True for valid dependencies.'''
        mock_base = Mock(spec=BaseBundle)
        dummy_service = DummyService()
        dummy_subprocessor = DummySubProcessor()
        dummy_cli = DummyCLI()

        dependencies = {
            'base': mock_base,
            'service': dummy_service,
            'subprocessor': dummy_subprocessor,
            'cli': dummy_cli
        }
        self.assertTrue(PicoSignBundleDependenciesValidator.is_valid(dependencies))

    def test_is_valid_failure(self) -> None:
        '''Tests is_valid returns False for invalid dependencies.'''
        self.assertFalse(PicoSignBundleDependenciesValidator.is_valid(None))  # type: ignore
        self.assertFalse(PicoSignBundleDependenciesValidator.is_valid("not_a_mapping"))  # type: ignore
        dependencies = {
            'base': Mock(spec=BaseBundle),
            'service': DummyService(),
            'subprocessor': DummySubProcessor()
        }
        self.assertFalse(PicoSignBundleDependenciesValidator.is_valid(dependencies))
