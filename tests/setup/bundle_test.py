# -*- coding: UTF-8 -*-

'''
Module
    bundle_test.py
Info
    Unit tests for PicoSignBundle class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock

from ats_utilities.base.setup.bundle import BaseBundle

from picosign.core.service.iservice import IService
from picosign.core.service.isubprocessor import ISubProcessor
from picosign.infrastructure.cli.icli import ICLI
from picosign.setup.bundle import PicoSignBundle


class TestPicoSignBundle(TestCase):
    '''Unit tests for PicoSignBundle.'''

    def test_bundle_creation_and_to_dict(self) -> None:
        '''Tests creating bundle and converting to dict.'''
        mock_base = Mock(spec=BaseBundle)
        mock_service = Mock(spec=IService)
        mock_subprocessor = Mock(spec=ISubProcessor)
        mock_cli = Mock(spec=ICLI)

        bundle = PicoSignBundle(
            base=mock_base,
            service=mock_service,
            subprocessor=mock_subprocessor,
            cli=mock_cli
        )

        self.assertEqual(bundle.base, mock_base)
        self.assertEqual(bundle.service, mock_service)
        self.assertEqual(bundle.subprocessor, mock_subprocessor)
        self.assertEqual(bundle.cli, mock_cli)

        bundle_dict = bundle.to_dict()
        self.assertIsInstance(bundle_dict, dict)
        self.assertTrue(isinstance(str(bundle), str))
