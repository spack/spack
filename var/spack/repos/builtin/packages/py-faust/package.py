# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFaust(PythonPackage):
    """Python Stream Processing."""

    homepage = "http://faust.readthedocs.io/"
    url      = "https://github.com/robinhood/faust/archive/v1.10.3.tar.gz"

    version('1.10.3', sha256='53d579e8dc20c0e681c2a1cfa36acca5e96b8295673bdbcc2cd6c9cc7a7142b0')
    version('1.10.2', sha256='a5d76cda148d07c93c0ffdbce8479dc77db99820f311c152d9b83acf1ad70b92')
    version('1.10.1', sha256='14255e0b1a1e1197ccdbfb6e14e17e4d6b14fb1b44522994ba7f3316337e97e7')
    version('1.10.0', sha256='2eac0e8a6ac18845196bd8c6c679f7b3ddadf7921d193a135b053e9a91a15dd1')
    version('1.9.0',  sha256='e5d110228f418e5653d71e3f8cbe2afb30a141cc6c04ee09cd50fbc2136af176')
    version('1.8.1',  sha256='b6b31dcbf07d2d95bda08fdc4a779dc7e021c6c661084d6cf99eecca1ba62492')
    version('1.8.0',  sha256='827f53d7f33b1ff1eb3a886f985c965c80d446455ddc0b16b18add37d68986e0')
    version('1.7.4',  sha256='3f92d1134853e87c85a68920feb70fa8e3ec3eaa1707eb5c0a121555514d22c3')
    version('1.7.3',  sha256='cd902696f4eaaf535e13abb053ee7f3bfd30482d8325a7ffc25dabddcae1851a')
    version('1.7.2',  sha256='6437fc0d64e5c697ad5e84e77ef2c46f7fb4c620525018530e8ba414e7c46820')

    depends_on('py-setuptools', type='build')
