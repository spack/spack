# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libfabric(AutotoolsPackage):
    """The Open Fabrics Interfaces (OFI) is a framework focused on exporting
       fabric communication services to applications."""

    homepage = "https://libfabric.org/"
    url      = "https://github.com/ofiwg/libfabric/releases/download/v1.6.1/libfabric-1.6.1.tar.gz"
    git      = "https://github.com/ofiwg/libfabric.git"

    version('develop', branch='master')
    version('1.8.0', sha256='c4763383a96af4af52cd81b3b094227f5cf8e91662f861670965994539b7ee37',
       url='https://github.com/ofiwg/libfabric/releases/download/v1.8.0/libfabric-1.8.0.tar.bz2')
    version('1.7.1', sha256='312e62c57f79b7274f89c41823932c00b15f1cc8de9c1f8dce17cd7fdae66fa1')
    version('1.7.0', sha256='9d7059e2ef48341f967f2a20ee215bc50f9079b32aad485f654098f83040e4be')
    version('1.6.2', sha256='b1a9cf8c47189a1c918f8b5710d05cb50df6b47a1c9b2ba51d927e97503b4df0')
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
               'mlx',
               'tcp',
               'efa')

    variant('fabrics',
            default='sockets',
            description='A list of enabled fabrics',
            values=fabrics,
            multi=True)

    # NOTE: the 'kdreg' variant enables use of the special /dev/kdreg file to
    #   assist in memory registration caching in the GNI provider.  This
    #   device file can only be opened once per process, however, and thus it
    #   frequently conflicts with MPI.
    variant('kdreg', default=False,
            description='Enable kdreg on supported Cray platforms')

    depends_on('rdma-core', when='fabrics=verbs')
    depends_on('opa-psm2', when='fabrics=psm2')
    depends_on('psm', when='fabrics=psm')
    depends_on('ucx', when='fabrics=mlx')

    depends_on('m4', when='@develop', type='build')
    depends_on('autoconf', when='@develop', type='build')
    depends_on('automake', when='@develop', type='build')
    depends_on('libtool', when='@develop', type='build')

    resource(name='fabtests',
             url='https://github.com/ofiwg/libfabric/releases/download/v1.7.0/fabtests-1.7.0.tar.gz',
             sha256='ebb4129dc69dc0e1f48310ce1abb96673d8ddb18166bc595312ebcb96e803de9',
             placement='fabtests', when='@1.7.0')
    resource(name='fabtests',
             url='https://github.com/ofiwg/fabtests/releases/download/v1.6.1/fabtests-1.6.1.tar.gz',
             sha256='d357466b868fdaf1560d89ffac4c4e93a679486f1b4221315644d8d3e21174bf',
             placement='fabtests', when='@1.6.1')
    resource(name='fabtests',
             url='https://github.com/ofiwg/fabtests/releases/download/v1.6.0/fabtests-1.6.0.tar.gz',
             sha256='dc3eeccccb005205017f5af60681ede15782ce202a0103450a6d56a7ff515a67',
             placement='fabtests', when='@1.6.0')
    resource(name='fabtests',
             url='https://github.com/ofiwg/fabtests/releases/download/v1.5.3/fabtests-1.5.3.tar.gz',
             sha256='3835b3bf86cd00d23df0ddba8bf317e4a195e8d5c3c2baa918b373d548f77f29',
             placement='fabtests', when='@1.5.3')
    resource(name='fabtests',
             url='https://github.com/ofiwg/fabtests/releases/download/v1.5.0/fabtests-1.5.0.tar.gz',
             sha256='1dddd446c3f1df346899f9a8636f1b4265de5b863103ae24876e9f0c1e40a69d',
             placement='fabtests', when='@1.5.0')
    resource(name='fabtests',
             url='https://github.com/ofiwg/fabtests/releases/download/v1.4.2/fabtests-1.4.2.tar.gz',
             sha256='3b78d0ca1b223ff21b7f5b3627e67e358e3c18b700f86b017e2233fee7e88c2e',
             placement='fabtests', when='@1.5.0')

    def setup_environment(self, spack_env, run_env):
        if self.run_tests:
            spack_env.prepend_path('PATH', self.prefix.bin)

    @when('@develop')
    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./autogen.sh')

        if self.run_tests:
            with working_dir('fabtests'):
                bash('./autogen.sh')

    def configure_args(self):
        args = []

        if '+kdreg' in self.spec:
            args.append('--with-kdreg=yes')
        else:
            args.append('--with-kdreg=no')

        for fabric in self.fabrics:
            if 'fabrics=' + fabric in self.spec:
                args.append('--enable-{0}=yes'.format(fabric))
            else:
                args.append('--enable-{0}=no'.format(fabric))

        return args

    def installcheck(self):
        fi_info = Executable(self.prefix.bin.fi_info)
        fi_info()

        # Build and run more extensive tests
        with working_dir('fabtests'):
            configure = Executable('./configure')
            configure('--prefix={0}'.format(self.prefix),
                      '--with-libfabric={0}'.format(self.prefix))
            make()
            make('install')
            make('test')
