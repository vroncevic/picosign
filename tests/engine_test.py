# -*- coding: UTF-8 -*-

'''
Module
    engine_test.py
Info
    Unit tests for PicoSign engine.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import Mock, patch

from ats_utilities.base.setup.factory import BaseBundleFactory
from ats_utilities.base.setup.options import BaseBundleOptions
from ats_utilities.context.factory import ContextBundleFactory
from ats_utilities.exceptions import ATSValueError

from picosign.engine import PicoSign
from picosign.setup.bundle import PicoSignBundle
from picosign.setup.factory import PicoSignBundleFactory
from picosign.core.service.iservice import IService
from picosign.core.service.isubprocessor import ISubProcessor
from picosign.infrastructure.cli.icli import ICLI


class DummyService(IService):
    '''Dummy service for testing.'''

    def execute(self, *, params: object) -> object:
        '''Executes service.'''
        return None

    def is_initialized(self) -> bool:
        '''Checks if service is initialized.'''
        return True

    def __str__(self) -> str:
        '''Returns string representation.'''
        return 'DummyService'


class DummySubProcessor(ISubProcessor):
    '''Dummy subprocessor for testing.'''

    def run(self, *, params: object) -> dict[str, object]:
        '''Runs subprocessor.'''
        return {}

    def is_initialized(self) -> bool:
        '''Checks if subprocessor is initialized.'''
        return True

    def __str__(self) -> str:
        '''Returns string representation.'''
        return 'DummySubProcessor'


class DummyCLI(ICLI):
    '''Dummy CLI for testing.'''

    def __init__(self, return_code: int = 0, stderr: str = '') -> None:
        '''Initializes dummy CLI.'''
        self.return_code = return_code
        self.stderr = stderr

    def run(self) -> dict[str, object]:
        '''Runs dummy CLI.'''
        return {'returncode': self.return_code, 'stderr': self.stderr}

    def is_initialized(self) -> bool:
        '''Checks if dummy CLI is initialized.'''
        return True

    def __str__(self) -> str:
        '''Returns string representation.'''
        return 'DummyCLI'


class TestPicoSign(TestCase):
    '''Unit tests for PicoSign engine.'''

    def test_engine_init_success(self) -> None:
        '''Tests successful initialization.'''
        bundle = PicoSignBundleFactory.create_bundle()
        engine = PicoSign(bundle)
        self.assertTrue(engine.is_initialized())

    def test_engine_init_fail_validation(self) -> None:
        '''Tests initialization failure on invalid bundle.'''
        engine = PicoSign(None)  # type: ignore
        self.assertFalse(engine.is_initialized())

    def test_engine_process_success(self) -> None:
        '''Tests successful engine processing.'''
        context_bundle = ContextBundleFactory.create_bundle()
        mock_base = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file='picosign/infrastructure/config/picosign.cfg',
                use_generator=False,
                context_bundle=context_bundle
            )
        )

        dummy_service = DummyService()
        dummy_subprocessor = DummySubProcessor()
        dummy_cli = DummyCLI(return_code=0)

        bundle = PicoSignBundle(
            base=mock_base,
            service=dummy_service,
            subprocessor=dummy_subprocessor,
            cli=dummy_cli
        )

        engine = PicoSign(bundle)
        self.assertTrue(engine.is_initialized())
        self.assertTrue(engine.process())

    def test_engine_process_cli_failure(self) -> None:
        '''Tests engine process with CLI failure.'''
        context_bundle = ContextBundleFactory.create_bundle()
        mock_base = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file='picosign/infrastructure/config/picosign.cfg',
                use_generator=False,
                context_bundle=context_bundle
            )
        )

        dummy_service = DummyService()
        dummy_subprocessor = DummySubProcessor()
        dummy_cli = DummyCLI(return_code=1, stderr='CLI error')

        bundle = PicoSignBundle(
            base=mock_base,
            service=dummy_service,
            subprocessor=dummy_subprocessor,
            cli=dummy_cli
        )

        engine = PicoSign(bundle)
        self.assertTrue(engine.is_initialized())
        self.assertFalse(engine.process())

    def test_engine_process_not_initialized(self) -> None:
        '''Tests engine process when not initialized.'''
        context_bundle = ContextBundleFactory.create_bundle()
        mock_base = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file='picosign/infrastructure/config/picosign.cfg',
                use_generator=False,
                context_bundle=context_bundle
            )
        )

        dummy_service = DummyService()
        dummy_subprocessor = DummySubProcessor()
        dummy_cli = DummyCLI()

        mock_base.option_manager.is_initialized = Mock(return_value=False)

        bundle = PicoSignBundle(
            base=mock_base,
            service=dummy_service,
            subprocessor=dummy_subprocessor,
            cli=dummy_cli
        )

        engine = PicoSign(bundle)
        self.assertFalse(engine.is_initialized())
        self.assertFalse(engine.process())

    def test_engine_process_exception(self) -> None:
        '''Tests engine process handling general exception.'''
        context_bundle = ContextBundleFactory.create_bundle()
        mock_base = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file='picosign/infrastructure/config/picosign.cfg',
                use_generator=False,
                context_bundle=context_bundle
            )
        )

        dummy_service = DummyService()
        dummy_subprocessor = DummySubProcessor()
        dummy_cli = DummyCLI()
        dummy_cli.run = Mock(side_effect=Exception('Unexpected error'))

        bundle = PicoSignBundle(
            base=mock_base,
            service=dummy_service,
            subprocessor=dummy_subprocessor,
            cli=dummy_cli
        )

        engine = PicoSign(bundle)
        self.assertTrue(engine.is_initialized())
        self.assertFalse(engine.process())

    def test_engine_process_validation_exception(self) -> None:
        '''Tests engine process handling ATS validation exception.'''
        context_bundle = ContextBundleFactory.create_bundle()
        mock_base = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file='picosign/infrastructure/config/picosign.cfg',
                use_generator=False,
                context_bundle=context_bundle
            )
        )

        dummy_service = DummyService()
        dummy_subprocessor = DummySubProcessor()
        dummy_cli = DummyCLI()
        dummy_cli.run = Mock(side_effect=ATSValueError('Validation error in run'))

        bundle = PicoSignBundle(
            base=mock_base,
            service=dummy_service,
            subprocessor=dummy_subprocessor,
            cli=dummy_cli
        )

        engine = PicoSign(bundle)
        self.assertTrue(engine.is_initialized())
        self.assertFalse(engine.process())

    @patch('picosign.setup.validator.PicoSignBundleValidator.validate')
    def test_engine_init_generic_exception(self, mock_validate: Mock) -> None:
        '''Tests engine init handling unexpected validation exception.'''
        mock_validate.side_effect = Exception('Unexpected generic validation error')

        context_bundle = ContextBundleFactory.create_bundle()
        mock_base = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file='picosign/infrastructure/config/picosign.cfg',
                use_generator=False,
                context_bundle=context_bundle
            )
        )

        dummy_service = DummyService()
        dummy_subprocessor = DummySubProcessor()
        dummy_cli = DummyCLI()

        bundle = PicoSignBundle(
            base=mock_base,
            service=dummy_service,
            subprocessor=dummy_subprocessor,
            cli=dummy_cli
        )

        engine = PicoSign(bundle)
        self.assertFalse(engine.is_initialized())
