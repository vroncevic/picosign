# -*- coding: UTF-8 -*-

'''
Module
    validator_test.py
Info
    Unit tests for PicoSignBundleValidator.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.exceptions import ATSValueError, ATSTypeError

from picosign.core.service.iservice import IService
from picosign.core.service.isubprocessor import ISubProcessor
from picosign.infrastructure.cli.icli import ICLI
from picosign.setup.bundle import PicoSignBundle
from picosign.setup.validator import PicoSignBundleValidator


class TestPicoSignBundleValidator(TestCase):
    '''Unit tests for PicoSignBundleValidator.'''

    def setUp(self) -> None:
        '''Sets up valid bundle.'''
        self.mock_base = Mock(spec=BaseBundle)
        self.mock_service = Mock(spec=IService)
        self.mock_sub = Mock(spec=ISubProcessor)
        self.mock_cli = Mock(spec=ICLI)

        self.bundle = PicoSignBundle(
            base=self.mock_base,
            service=self.mock_service,
            subprocessor=self.mock_sub,
            cli=self.mock_cli
        )

    def test_validate_success(self) -> None:
        '''Tests validation pass.'''
        self.assertTrue(PicoSignBundleValidator.is_valid(self.bundle))
        PicoSignBundleValidator.validate(self.bundle)

    def test_validate_none_bundle(self) -> None:
        '''Tests validation with None bundle.'''
        self.assertFalse(PicoSignBundleValidator.is_valid(None))  # type: ignore
        with self.assertRaises((ATSValueError, ATSTypeError)):
            PicoSignBundleValidator.validate(None)  # type: ignore
