# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lzo(AutotoolsPackage):
    """Real-time data compression library"""

    homepage = 'https://www.oberhumer.com/opensource/lzo/'
    url = 'http://www.oberhumer.com/opensource/lzo/download/lzo-2.09.tar.gz'

    version('2.09', 'c7ffc9a103afe2d1bba0b015e7aa887f')
    version('2.08', 'fcec64c26a0f4f4901468f360029678f')
    version('2.07', '4011935e95171e78ad4894f7335c982a')
    version('2.06', '95380bd4081f85ef08c5209f4107e9f8')
    version('2.05', 'c67cda5fa191bab761c7cb06fe091e36')

    def configure_args(self):
        return [
            '--disable-dependency-tracking',
            '--enable-shared'
        ]
