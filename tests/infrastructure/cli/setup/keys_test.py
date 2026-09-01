# -*- coding: UTF-8 -*-

'''
Module
    keys_test.py
Info
    Unit tests for CLIBundleKeys class.
'''

from __future__ import annotations

from unittest import TestCase

from picosign.infrastructure.cli.setup.keys import CLIBundleKeys


class TestCLIBundleKeys(TestCase):
    '''Unit tests for CLIBundleKeys.'''

    def test_keys_definitions(self) -> None:
        '''Tests constants and type mappings.'''
        dep_types = CLIBundleKeys.get_dependency_to_type()
        self.assertIn(CLIBundleKeys.DEPENDENCY_SERVICE, dep_types)
        self.assertIn(CLIBundleKeys.DEPENDENCY_PARSER, dep_types)
        self.assertIn(CLIBundleKeys.DEPENDENCY_COMMANDS, dep_types)

        opt_types = CLIBundleKeys.get_option_to_type()
        self.assertIn(CLIBundleKeys.OPTION_SERVICE, opt_types)
        self.assertIn(CLIBundleKeys.OPTION_PARSER, opt_types)
