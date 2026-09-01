# -*- coding: UTF-8 -*-

'''
Module
    registry_test.py
Info
    Unit tests for PicoSignBundleRegistry class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock

from ats_utilities.base.setup.bundle import BaseBundle

from picosign.setup.bundle import PicoSignBundle
from picosign.setup.registry import PicoSignBundleRegistry
from picosign.core.service.iservice import IService
from picosign.core.service.isubprocessor import ISubProcessor
from picosign.infrastructure.cli.icli import ICLI


class DummyService(IService):
    '''Dummy service for testing.'''

    def execute(self, *, params: object) -> object:
        '''Executes service.'''
        return None

    def is_initialized(self) -> bool:
        '''Checks initialized.'''
        return True


class DummySubProcessor(ISubProcessor):
    '''Dummy subprocessor for testing.'''

    def run(self, *, params: object) -> dict[str, object]:
        '''Runs subprocessor.'''
        return {}

    def is_initialized(self) -> bool:
        '''Checks initialized.'''
        return True


class DummyCLI(ICLI):
    '''Dummy CLI for testing.'''

    def run(self) -> dict[str, object]:
        '''Runs CLI.'''
        return {}

    def is_initialized(self) -> bool:
        '''Checks initialized.'''
        return True


class TestPicoSignBundleRegistry(TestCase):
    '''Unit tests for PicoSignBundleRegistry.'''

    def test_create_bundle_success(self) -> None:
        '''Tests creating bundle from registry.'''
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

        bundle = PicoSignBundleRegistry.create_bundle(dependencies)
        self.assertIsInstance(bundle, PicoSignBundle)
        self.assertEqual(bundle.base, mock_base)

    def test_create_bundle_invalid_dependencies(self) -> None:
        '''Tests creating bundle with invalid dependencies raises error.'''
        with self.assertRaises(Exception):
            PicoSignBundleRegistry.create_bundle(None)  # type: ignore

    def test_get_version(self) -> None:
        '''Tests get_version method.'''
        self.assertEqual(PicoSignBundleRegistry.get_version(), '1.0.0')
