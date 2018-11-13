# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libfabric(AutotoolsPackage):
    """The Open Fabrics Interfaces (OFI) is a framework focused on exporting
       fabric communication services to applications."""

    homepage = "https://libfabric.org/"
    url      = "https://github.com/ofiwg/libfabric/releases/download/v1.6.1/libfabric-1.6.1.tar.gz"
    git = "https://github.com/ofiwg/libfabric.git"

    version('develop', branch='master')
    version('1.6.1', 'ff78dc9fcbf273a119c737a4e1df46d1')
    version('1.6.0', '91d63ab3c0b9724a4db660019f928cab')
    version('1.5.3', '1fe07e972fe487c6a3e44c0fb68b49a2')
    version('1.5.0', 'fda3e9b31ebe184f5157288d059672d6')
    version('1.4.2', '2009c8e0817060fb99606ddbf6c5ccf8')

    fabrics = ('psm',
               'psm2',
               'sockets',
               'verbs',
               'usnic',
               'gni',
               'xpmem',
               'udp',
               'rxm',
               'rxd',
               'mlx')

    variant(
       'fabrics',
       default='sockets',
       description='A list of enabled fabrics',
       values=fabrics,
       multi=True
    )

    depends_on('rdma-core', when='fabrics=verbs')
    depends_on('opa-psm2', when='fabrics=psm2')
    depends_on('psm', when='fabrics=psm')
    depends_on('ucx', when='fabrics=mlx')

    depends_on('m4', when='@develop', type='build')
    depends_on('autoconf', when='@develop', type='build')
    depends_on('automake', when='@develop', type='build')
    depends_on('libtool', when='@develop', type='build')

    @when('@develop')
    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./autogen.sh')

    def configure_args(self):
        args = []

        args.extend(['--enable-%s=%s' %
                     (f, 'yes' if 'fabrics=%s' % f in self.spec else 'no')
                     for f in self.fabrics])

        return args
