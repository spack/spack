# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Opencoarrays(CMakePackage):
    """OpenCoarrays is an open-source software project that produces an
    application binary interface (ABI) supporting coarray Fortran (CAF)
    compilers, an application programming interface (API) that supports users
    of non-CAF compilers, and an associated compiler wrapper and program
    launcher.
    """

    homepage = "http://www.opencoarrays.org/"
    url      = "https://github.com/sourceryinstitute/OpenCoarrays/releases/download/2.2.0/OpenCoarrays-2.2.0.tar.gz"

    version('2.7.1', 'd74ee914f94de1c396b96bbad2cf43d68f29fcc87460fcc0db6582e6ae691588')
    version('2.2.0', '9311547a85a21853111f1e8555ceab4593731c6fd9edb64cfb9588805f9d1a0d')
    version('1.8.10', '9ba1670647db4d986634abf743abfd6a')
    version('1.8.4', '7c9eaffc3a0b5748d0d840e52ec9d4ad')
    version('1.8.0', 'ca78d1507b2a118c75128c6c2e093e27')
    version('1.7.4', '85ba87def461e3ff5a164de2e6482930')
    version('1.6.2', '5a4da993794f3e04ea7855a6678981ba')

    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo',
                    'MinSizeRel', 'CodeCoverage'))

    depends_on('mpi')
    # This patch removes a bunch of checks for the version of MPI available on
    # the system. They make the Crays hang.
    patch('CMakeLists.patch', when='platform=cray')

    def cmake_args(self):
        args = []
        args.append("-DCMAKE_C_COMPILER=%s" % self.spec['mpi'].mpicc)
        args.append("-DCMAKE_Fortran_COMPILER=%s" % self.spec['mpi'].mpifc)
        return args
