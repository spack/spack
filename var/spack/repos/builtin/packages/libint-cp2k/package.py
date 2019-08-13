# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LibintCp2k(CMakePackage):
    """libint configured for CP2K."""

    homepage = "https://github.com/cp2k/libint-cp2k"

    version('2.6.0', sha256='1cd72206afddb232bcf2179c6229fbf6e42e4ba8440e701e6aa57ff1e871e9db')

    depends_on('python', type='build')
    depends_on('boost')

    def url_for_version(self, version):
        url = 'https://github.com/cp2k/libint-cp2k/releases/download/v{0}/libint-v{0}-cp2k-lmax-{1}.tgz'

        return url.format(version, 5)

    def cmake_args(self):
        return ['-DENABLE_FORTRAN=ON']
