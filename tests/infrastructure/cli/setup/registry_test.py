# -*- coding: UTF-8 -*-

'''
Module
    registry_test.py
Info
    Unit tests for CLIBundleRegistry class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock

from ats_utilities.option.imanager import IOptionManager

from picosign.core.service.iservice import IService
from picosign.infrastructure.command.command import CommandBundle
from picosign.infrastructure.cli.setup.bundle import CLIBundle
from picosign.infrastructure.cli.setup.registry import CLIBundleRegistry


class TestCLIBundleRegistry(TestCase):
    '''Unit tests for CLIBundleRegistry.'''

    def test_create_bundle_success(self) -> None:
        '''Tests registry create_bundle.'''
        mock_service = Mock(spec=IService)
        mock_parser = Mock(spec=IOptionManager)
        mock_command = Mock(spec=CommandBundle)

        dependencies = {
            'service': mock_service,
            'parser': mock_parser,
            'commands': [mock_command]
        }
        bundle = CLIBundleRegistry.create_bundle(dependencies)
        self.assertIsInstance(bundle, CLIBundle)

    def test_create_bundle_failure(self) -> None:
        '''Tests registry failure.'''
        with self.assertRaises(Exception):
            CLIBundleRegistry.create_bundle(None)  # type: ignore

    def test_get_version(self) -> None:
        '''Tests get_version.'''
        self.assertEqual(CLIBundleRegistry.get_version(), '1.0.0')
