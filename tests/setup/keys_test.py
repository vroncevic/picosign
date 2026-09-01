# -*- coding: UTF-8 -*-

'''
Module
    keys_test.py
Info
    Unit tests for PicoSignBundleKeys.
'''

from __future__ import annotations

from unittest import TestCase

from picosign.setup.keys import PicoSignBundleKeys


class TestPicoSignBundleKeys(TestCase):
    '''Unit tests for PicoSignBundleKeys.'''

    def test_keys_definitions(self) -> None:
        '''Tests constants and type mappings.'''
        dep_types = PicoSignBundleKeys.get_dependency_to_type()
        self.assertIn(PicoSignBundleKeys.DEPENDENCY_BASE, dep_types)
        self.assertIn(PicoSignBundleKeys.DEPENDENCY_SERVICE, dep_types)
        self.assertIn(PicoSignBundleKeys.DEPENDENCY_SUBPROCESSOR, dep_types)
        self.assertIn(PicoSignBundleKeys.DEPENDENCY_CLI, dep_types)

        opt_types = PicoSignBundleKeys.get_option_to_type()
        self.assertIn(PicoSignBundleKeys.OPTION_INFO_FILE, opt_types)
