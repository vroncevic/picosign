# -*- coding: UTF-8 -*-

'''
Module
    signature_data_test.py
Info
    Unit tests for SignatureData domain model.
'''

from __future__ import annotations

from unittest import TestCase

from picosign.core.model.signature_data import SignatureData


class TestSignatureData(TestCase):
    '''Unit tests for SignatureData.'''

    def test_signature_data_creation(self) -> None:
        '''Tests creating SignatureData.'''
        data = SignatureData(file_path='test.uf2', signature='test_sig', output_path='out.uf2')
        self.assertEqual(data.file_path, 'test.uf2')
        self.assertEqual(data.signature, 'test_sig')
        self.assertEqual(data.output_path, 'out.uf2')

    def test_signature_data_defaults(self) -> None:
        '''Tests default values for SignatureData.'''
        data = SignatureData(file_path='test.uf2')
        self.assertEqual(data.file_path, 'test.uf2')
        self.assertIsNone(data.signature)
        self.assertIsNone(data.output_path)
