# -*- coding: UTF-8 -*-

'''
Module
    opt_validator_test.py
Info
    Unit tests for PicoSignBundleOptionsValidator class.
'''

from __future__ import annotations

from unittest import TestCase

from picosign.setup.opt_validator import PicoSignBundleOptionsValidator


class TestPicoSignBundleOptionsValidator(TestCase):
    '''Unit tests for PicoSignBundleOptionsValidator.'''

    def test_validate_success(self) -> None:
        '''Tests successful options validation.'''
        options = {'info_file': 'some_path'}
        PicoSignBundleOptionsValidator.validate(options)

    def test_validate_none(self) -> None:
        '''Tests validate None raises error.'''
        with self.assertRaises(Exception):
            PicoSignBundleOptionsValidator.validate(None)  # type: ignore

    def test_validate_invalid_type(self) -> None:
        '''Tests validate invalid type raises error.'''
        with self.assertRaises(Exception):
            PicoSignBundleOptionsValidator.validate("not_a_mapping")  # type: ignore

        with self.assertRaises(Exception):
            options = {'info_file': 123}
            PicoSignBundleOptionsValidator.validate(options)  # type: ignore

    def test_is_valid_success(self) -> None:
        '''Tests is_valid returns True for valid options.'''
        options = {'info_file': 'some_path'}
        self.assertTrue(PicoSignBundleOptionsValidator.is_valid(options))

    def test_is_valid_failure(self) -> None:
        '''Tests is_valid returns False for invalid options.'''
        self.assertFalse(PicoSignBundleOptionsValidator.is_valid(None))  # type: ignore
        self.assertFalse(PicoSignBundleOptionsValidator.is_valid("not_a_mapping"))  # type: ignore
        self.assertFalse(PicoSignBundleOptionsValidator.is_valid({'info_file': 123}))  # type: ignore
