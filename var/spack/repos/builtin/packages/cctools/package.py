# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cctools(AutotoolsPackage):
    """The Cooperative Computing Tools (cctools) enable large scale
       distributed computations to harness hundreds to thousands of
       machines from clusters, clouds, and grids.
    """

    homepage = "https://github.com/cooperative-computing-lab/cctools"
    url      = "https://github.com/cooperative-computing-lab/cctools/archive/release/6.1.1.tar.gz"

    version('6.1.1', '9b43cdb3aceebddc1608c77184590619')

    depends_on('openssl')
    depends_on('perl+shared', type=('build', 'run'))
    depends_on('python@:3', type=('build', 'run'))
    depends_on('readline')
    depends_on('swig')
    # depends_on('xrootd')
    depends_on('zlib')
    patch('arm.patch', when='target=aarch64:')

    # Generally SYS_foo is defined to __NR_foo (sys/syscall.h) which
    # is then defined to a syscall number (asm/unistd_64.h).  Certain
    # CentOS systems have SYS_memfd_create defined to
    # __NR_memfd_create but are missing the second definition.
    # This is a belt and suspenders solution to the problem.
    def patch(self):
        before = '#if defined(__linux__) && defined(SYS_memfd_create)'
        after = '#if defined(__linux__) && defined(SYS_memfd_create) && defined(__NR_memfd_create)'  # noqa: E501
        f = 'dttools/src/memfdexe.c'
        kwargs = {'ignore_absent': False, 'backup': True, 'string': True}
        filter_file(before, after, f, **kwargs)

    def configure_args(self):
        args = []
        # disable these bits
        for p in ['mysql', 'python3', 'xrootd']:
            args.append('--with-{0}-path=no'.format(p))
        # point these bits at the Spack installations
        for p in ['openssl', 'perl', 'python', 'readline', 'swig', 'zlib']:
            args.append('--with-{0}-path={1}'.format(p, self.spec[p].prefix))
        return args
