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
    version('1.5', sha256='892f3623c73254d40fbbb8cbc3056219a31510e37aae2ede4100c04743701a5c')
    version('1.4', sha256='d5d12aedb9e97f079c4428aaa486bfa4e31fe1db547e103c52e76c8ec906d0a8')
    version('1.3', sha256='3817ea57045443c1a9a819560911db1175dbe4153e317adaa1492437f3f13f3b', deprecated=True)
    version('1.2', sha256='126a7e01d79458807a6545a8e5f92f8d62a23187dee70be0913b60a1393780e0', deprecated=True)
    version('1.1', sha256='2bbdacf3e0ce4e7c9e360874d8d85b405525bdc7bd992bdb1f1ba49218072160', deprecated=True)
    version('1.0', sha256='d594b73d6549a61fce8e67b8984a17cebc3e766fc520ed1636ae3683cdde77cb', deprecated=True)

    depends_on('libpthread-stubs')
    depends_on('mpi')
    depends_on('er')
    depends_on('axl')
    depends_on('openssl')
    depends_on('cmake@3.9:', type='build')

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
