# -*- coding: UTF-8 -*-

'''
Module
    engine_test.py
Info
    Unit tests for core Service.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock

from picosign.core.service.engine import Service
from picosign.core.service.isubprocessor import ISubProcessor


class DummySubProcessor(ISubProcessor):
    '''Dummy subprocessor for testing.'''

    def run(self, *, params: object) -> object:
        '''Runs subprocessor.'''
        return {'returncode': 0, 'stdout': 'ok', 'stderr': ''}

    def is_initialized(self) -> bool:
        '''Checks initialized.'''
        return True


class TestService(TestCase):
    '''Unit tests for Service.'''

    def test_init_success(self) -> None:
        '''Tests successful initialization.'''
        sub = DummySubProcessor()
        srv = Service(subprocessor=sub)
        self.assertTrue(srv.is_initialized())

    def test_init_errors(self) -> None:
        '''Tests initialization errors with invalid arguments.'''
        with self.assertRaises(ValueError):
            Service(subprocessor=None)  # type: ignore

        with self.assertRaises(TypeError):
            Service(subprocessor='invalid')  # type: ignore

    def test_execute(self) -> None:
        '''Tests service execution.'''
        sub = DummySubProcessor()
        sub.run = Mock(return_value={'returncode': 0, 'stdout': 'done', 'stderr': ''})
        srv = Service(subprocessor=sub)
        result = srv.execute(params={'action': 'read', 'file': 'test.uf2'})
        self.assertEqual(result.get('returncode'), 0)
        sub.run.assert_called_once_with(params={'action': 'read', 'file': 'test.uf2'})
