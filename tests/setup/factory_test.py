# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
Info
    Unit tests for PicoSignBundleFactory.
'''

from __future__ import annotations

from unittest import TestCase

from picosign.setup.factory import PicoSignBundleFactory
from picosign.setup.bundle import PicoSignBundle
from picosign.setup.options import PicoSignBundleOptions


class TestPicoSignBundleFactory(TestCase):
    '''Unit tests for PicoSignBundleFactory.'''

    def test_create_bundle_default(self) -> None:
        '''Tests creating bundle with default configuration.'''
        bundle = PicoSignBundleFactory.create_bundle()
        self.assertIsInstance(bundle, PicoSignBundle)
        self.assertIsNotNone(bundle.base)
        self.assertIsNotNone(bundle.service)
        self.assertIsNotNone(bundle.subprocessor)
        self.assertIsNotNone(bundle.cli)

    def test_create_bundle_with_options(self) -> None:
        '''Tests creating bundle with custom options.'''
        options = PicoSignBundleOptions(info_file='picosign/infrastructure/config/picosign.cfg')
        bundle = PicoSignBundleFactory.create_bundle(options=options)
        self.assertIsInstance(bundle, PicoSignBundle)

    def test_get_version(self) -> None:
        '''Tests factory get_version.'''
        self.assertEqual(PicoSignBundleFactory.get_version(), '1.0.0')
