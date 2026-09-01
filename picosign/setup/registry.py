# -*- coding: UTF-8 -*-

'''
Module
    registry.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    picosign is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    picosign is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Encapsulates core picosign components for simplification of picosign bundle.
'''

from __future__ import annotations

from ats_utilities.base.setup.bundle import BaseBundle

from picosign.core.service.iservice import IService
from picosign.core.service.isubprocessor import ISubProcessor
from picosign.infrastructure.cli.icli import ICLI
from picosign.setup.bundle import PicoSignBundle
from picosign.setup.validator import PicoSignBundleValidator
from picosign.setup.keys import PicoSignBundleKeys
from picosign.setup.dependencies import PicoSignBundleDependencies
from picosign.setup.dep_validator import PicoSignBundleDependenciesValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/picosign'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/picosign/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PicoSignBundleRegistry:
    '''
        Encapsulates core picosign components for simplification of picosign bundle.

        It defines:

            :methods:
                | create_bundle - Creates the picosign bundle.
                | get_version - Returns the registry version.
    '''

    @classmethod
    def create_bundle(cls, dependencies: PicoSignBundleDependencies) -> PicoSignBundle:
        '''
            Creates the picosign bundle.

            :param dependencies: The picosign bundle dependencies.
            :return: The picosign bundle.
            :exceptions:
                | ATSValueError: The picosign bundle dependencies must be provided and have proper values.
                | ATSTypeError:  The picosign bundle dependencies must be an instance of Mapping and its
                |                attributes must be instances of their respective types.
                | ATSValueError: The picosign bundle must be provided and have proper values.
                | ATSTypeError:  The picosign bundle must be an instance of PicoSignBundle and
                |                its attributes must be instances of their respective types.
        '''
        PicoSignBundleDependenciesValidator.validate(dependencies)

        base: BaseBundle | None = dependencies.get(PicoSignBundleKeys.DEPENDENCY_BASE) if dependencies else None
        service: IService | None = dependencies.get(PicoSignBundleKeys.DEPENDENCY_SERVICE) if dependencies else None
        subprocessor: ISubProcessor | None = dependencies.get(PicoSignBundleKeys.DEPENDENCY_SUBPROCESSOR) if dependencies else None
        cli: ICLI | None = dependencies.get(PicoSignBundleKeys.DEPENDENCY_CLI) if dependencies else None

        bundle: PicoSignBundle = PicoSignBundle(base=base, service=service, subprocessor=subprocessor, cli=cli)
        PicoSignBundleValidator.validate(bundle)

        return bundle

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the registry version.

            :return: The registry version.
            :exceptions: None.
        '''
        return __version__
