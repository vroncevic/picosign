# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
Info
    Unit tests for CLIBundleFactory class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock

from ats_utilities.option.imanager import IOptionManager

from picosign.core.service.iservice import IService
from picosign.infrastructure.cli.setup.bundle import CLIBundle
from picosign.infrastructure.cli.setup.options import CLIBundleOptions
from picosign.infrastructure.cli.setup.factory import CLIBundleFactory


class TestCLIBundleFactory(TestCase):
    '''Unit tests for CLIBundleFactory.'''

    def test_create_bundle_success(self) -> None:
        '''Tests factory create_bundle.'''
        mock_service = Mock(spec=IService)
        mock_parser = Mock(spec=IOptionManager)

        options = CLIBundleOptions(service=mock_service, parser=mock_parser)
        bundle = CLIBundleFactory.create_bundle(options=options)
        self.assertIsInstance(bundle, CLIBundle)
        self.assertEqual(len(bundle.commands), 2)

    def test_create_bundle_invalid_options(self) -> None:
        '''Tests factory create_bundle with invalid options.'''
        with self.assertRaises(Exception):
            CLIBundleFactory.create_bundle(options='invalid')  # type: ignore

    def test_get_version(self) -> None:
        '''Tests factory get_version.'''
        self.assertEqual(CLIBundleFactory.get_version(), '1.0.0')
