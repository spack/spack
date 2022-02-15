# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Veloc(CMakePackage):
    """Very-Low Overhead Checkpointing System. VELOC is a multi-level
    checkpoint-restart runtime for HPC supercomputing infrastructures"""

    homepage = "https://github.com/ECP-VeloC/VELOC"
    url      = "https://github.com/ECP-VeloC/VELOC/archive/1.6.tar.gz"
    git      = "https://github.com/ecp-veloc/veloc.git"
    maintainers = ['bnicolae']
    tags = ['e4s']

    version('main', branch='main')
    version('1.6', sha256='451b46ad13e360270044c0dba09d8e4fbd64149f8e8d71310fdb520424c5eeaa')

    depends_on('libpthread-stubs')
    depends_on('mpi')
    depends_on('er')
    depends_on('axl@0.5.0:')
    depends_on('openssl')
    depends_on('cmake@3.10:', type='build')

    depends_on('boost', when='@:1.5')

    def flag_handler(self, name, flags):
        flags = list(flags)
        if name == 'cxxflags':
            if self.spec.satisfies('@:1.5'):
                flags.append(self.compiler.cxx11_flag)
            else:
                flags.append(self.compiler.cxx17_flag)
            
        return (None, None, flags)

    def cmake_args(self):
        args = [
            "-DWITH_AXL_PREFIX=%s" % self.spec['axl'].prefix,
            "-DWITH_ER_PREFIX=%s" % self.spec['er'].prefix,
            "-DMPI_CXX_COMPILER=%s" % self.spec['mpi'].mpicxx
        ]

        if self.spec.satisfies('@:1.5'):
            args.append("-DBOOST_ROOT=%s" % self.spec['boost'].prefix)

        if self.spec.satisfies('@1.6:'):
            args.append("-DCOMM_QUEUE=socket_queue")

        return args
