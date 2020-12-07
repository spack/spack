# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Openwsman(CMakePackage):
    """Openwsman server implementation and client api with bindings."""

    homepage = "https://github.com/Openwsman/openwsman"
    url      = "https://github.com/Openwsman/openwsman/archive/v2.6.11.tar.gz"

    version('2.7.0',  sha256='8870c4a21cbaba9387ad38c37667e2cee29008faacaaf7eb18ad2061e2fc89a1')
    version('2.6.11', sha256='895eaaae62925f9416766ea3e71a5368210e6cfe13b23e4e0422fa0e75c2541c')
    version('2.6.10', sha256='d3c624a03d7bc1835544ce1af56efd010f77cbee0c02b34e0755aa9c9b2c317b')

    depends_on('python@3:', type='build')
    depends_on('curl')
    depends_on('libxml2')
    depends_on('sblim-sfcc')

    def cmake_args(self):
        return ['-DBUILD_PYTHON=OFF', '-DUSE_PAM=NO']
