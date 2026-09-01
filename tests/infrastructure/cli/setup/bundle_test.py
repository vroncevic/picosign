# -*- coding: UTF-8 -*-

'''
Module
    bundle_test.py
Info
    Unit tests for CLIBundle class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock

from ats_utilities.option.imanager import IOptionManager

from picosign.core.service.iservice import IService
from picosign.infrastructure.cli.setup.bundle import CLIBundle
from picosign.infrastructure.command.command import CommandBundle


class TestCLIBundle(TestCase):
    '''Unit tests for CLIBundle.'''

    def test_bundle_creation_and_to_dict(self) -> None:
        '''Tests creating CLIBundle and converting to dict.'''
        mock_service = Mock(spec=IService)
        mock_parser = Mock(spec=IOptionManager)
        mock_command = Mock(spec=CommandBundle)

        bundle = CLIBundle(
            service=mock_service,
            parser=mock_parser,
            commands=[mock_command]
        )

        self.assertEqual(bundle.service, mock_service)
        self.assertEqual(bundle.parser, mock_parser)
        self.assertEqual(bundle.commands, [mock_command])

        bundle_dict = bundle.to_dict()
        self.assertIsInstance(bundle_dict, dict)
        self.assertTrue(isinstance(str(bundle), str))
