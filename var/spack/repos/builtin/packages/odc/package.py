# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Odc(CMakePackage):
    """ECMWF encoding and decoding of observational data in ODB2 format."""

    homepage = 'https://github.com/ecmwf/odc'
    url = 'https://github.com/ecmwf/odc/archive/refs/tags/1.3.0.tar.gz'

    maintainers = ['skosukhin']

    version('1.3.0', sha256='97a4f10765b341cc8ccbbf203f5559cb1b838cbd945f48d4cecb1bc4305e6cd6')

    variant('fortran', default=False,
            description='Enable the Fortran interface')

    depends_on('ecbuild@3.4:', type='build')
    depends_on('cmake@3.12:', type='build')

    depends_on('eckit@1.4:+sql')

    def cmake_args(self):
        args = [
            self.define_from_variant('ENABLE_FORTRAN', 'fortran'),
            # The tests download additional data (~650MB):
            self.define('ENABLE_TESTS', self.run_tests)
        ]
        return args
