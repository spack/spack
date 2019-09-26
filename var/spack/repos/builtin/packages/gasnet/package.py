# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gasnet(AutotoolsPackage):
    """GASNet is a language-independent, low-level networking layer
       that provides network-independent, high-performance communication
       primitives tailored for implementing parallel global address space
       SPMD languages and libraries such as UPC, Co-Array Fortran, SHMEM,
       Cray Chapel, and Titanium.
    """
    homepage = "http://gasnet.lbl.gov"
    url      = "http://gasnet.lbl.gov/download/GASNet-1.24.0.tar.gz"

    version('2019.3.0', sha256='97fe19bb5ab32d14a96d2dd19d0f03048f68bb20ca83abe0c00cdab40e86eba5')
    version('1.32.0', sha256='42e4774b3bbc7c142f77c41b6ce86b594f579073f46c31f47f424c7e31ee1511')
    version('1.30.0', '2ddb1d8397d62acfd389095ca8da72f6')
    version('1.28.2', '6ca0463dc2430570e40646c4d1e97b36')
    version('1.28.0', 'b44446d951d3d8954aa1570e3556ba61')
    version('1.24.0', 'c8afdf48381e8b5a7340bdb32ca0f41a')

    variant('ibv', default=False, description="Support InfiniBand")
    variant('mpi', default=True, description="Support MPI")
    variant('aligned-segments', default=False,
            description="Requirement to achieve aligned VM segments")
    variant('pshm', default=True,
            description="Support inter-process shared memory support")
    variant('segment-mmap-max', default='16GB',
            description="Upper bound for mmap-based GASNet segments")

    conflicts('+aligned-segments', when='+pshm')

    depends_on('mpi', when='+mpi')

    def url_for_version(self, version):
        url = "http://gasnet.lbl.gov/"
        if version >= Version('2019'):
            url += "EX/GASNet-{0}.tar.gz".format(version)
        else:
            url += "download/GASNet-{0}.tar.gz".format(version)

        return url

    def configure_args(self):
        args = [
            # TODO: factor IB suport out into architecture description.
            "--enable-par",
            "--enable-mpi-compat",
            # for consumers with shared libs
            "CC=%s %s" % (spack_cc, self.compiler.pic_flag),
            "CXX=%s %s" % (spack_cxx, self.compiler.pic_flag),
        ]

        if '+aligned-segments' in self.spec:
            args.append('--enable-aligned-segments')
        else:
            args.append('--disable-aligned-segments')

        if '+mpi' in self.spec:
            args.extend(['--enable-mpi',
                         '--disable-udp',
                         '--disable-ibv',
                         'MPI_CC=%s %s'
                        % (self.spec['mpi'].mpicc, self.compiler.pic_flag)])

        if '+ibv' in self.spec:
            args.extend(['--enable-ibv', '--disable-udp', '--disable-mpi'])

        if '+udp' in self.spec:
            args.extend(['--enable-udp', '--disable-ibv', '--disable-mpi'])

        return args
