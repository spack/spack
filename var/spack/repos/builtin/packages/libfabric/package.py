# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path
from spack import *


class Libfabric(AutotoolsPackage):
    """The Open Fabrics Interfaces (OFI) is a framework focused on exporting
       fabric communication services to applications."""

    homepage = "https://libfabric.org/"
    url      = "https://github.com/ofiwg/libfabric/releases/download/v1.6.1/libfabric-1.6.1.tar.gz"
    git      = "https://github.com/ofiwg/libfabric.git"

    version('develop', branch='master')
    version('1.9.0', sha256='559bfb7376c38253c936d0b104591c3394880376d676894895706c4f5f88597c',
       url='https://github.com/ofiwg/libfabric/releases/download/v1.9.0/libfabric-1.9.0.tar.bz2')
    version('1.8.1', sha256='3c560b997f9eafd89f961dd8e8a29a81aad3e39aee888e3f3822da419047dc88',
       url='https://github.com/ofiwg/libfabric/releases/download/v1.8.1/libfabric-1.8.1.tar.bz2')
    version('1.8.0', sha256='c4763383a96af4af52cd81b3b094227f5cf8e91662f861670965994539b7ee37',
       url='https://github.com/ofiwg/libfabric/releases/download/v1.8.0/libfabric-1.8.0.tar.bz2')
    version('1.7.1', sha256='312e62c57f79b7274f89c41823932c00b15f1cc8de9c1f8dce17cd7fdae66fa1')
    version('1.7.0', sha256='9d7059e2ef48341f967f2a20ee215bc50f9079b32aad485f654098f83040e4be')
    version('1.6.2', sha256='b1a9cf8c47189a1c918f8b5710d05cb50df6b47a1c9b2ba51d927e97503b4df0')
    version('1.6.1', sha256='ac85f18bbf09226e868d72771ecba39cfdb7915aab3aeb855c95f8be7817f8bc')
    version('1.6.0', sha256='cd7d4543cf706820e4a33003457eff97336b5160f35d0e8b001aea18b5470423')
    version('1.5.3', sha256='770e505185074b4c66a0c33ac2155670142746a71a6299c286f6d5cd220cbff8')
    version('1.5.0', sha256='f62709e70fab6abea719402da854f3c6ab60369be6b1e31e4f77554c7454da28')
    version('1.4.2', sha256='858e30d92b69ee5e47ac10a8ac0c731b491d75a6e28267a128f3d6eb43f940a1')

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
               'efa',
               'mrail',
               'shm')

    variant('fabrics',
            default='sockets,tcp,udp',
            description='A list of enabled fabrics',
            values=fabrics,
            multi=True)

    # NOTE: the 'kdreg' variant enables use of the special /dev/kdreg file to
    #   assist in memory registration caching in the GNI provider.  This
    #   device file can only be opened once per process, however, and thus it
    #   frequently conflicts with MPI.
    variant('kdreg', default=False,
            description='Enable kdreg on supported Cray platforms')

    # For version 1.9.0:
    # headers: fix forward-declaration of enum fi_collective_op with C++
    patch('https://github.com/ofiwg/libfabric/commit/2e95b0efd85fa8a3d814128e34ec57ffd357460e.patch',
          sha256='71f06e8bf0adeccd425b194ac524e4d596469e9dab9e7a4f8bb209e6b9a454f4',
          when='@1.9.0')

    depends_on('rdma-core', when='fabrics=verbs')
    depends_on('opa-psm2', when='fabrics=psm2')
    depends_on('psm', when='fabrics=psm')
    depends_on('ucx', when='fabrics=mlx')

    depends_on('m4', when='@develop', type='build')
    depends_on('autoconf', when='@develop', type='build')
    depends_on('automake', when='@develop', type='build')
    depends_on('libtool', when='@develop', type='build')

    resource(name='fabtests',
             url='https://github.com/ofiwg/libfabric/releases/download/v1.9.0/fabtests-1.9.0.tar.bz2',
             sha256='60cc21db7092334904cbdafd142b2403572976018a22218e7c453195caef366e',
             placement='fabtests', when='@1.9.0')
    resource(name='fabtests',
             url='https://github.com/ofiwg/libfabric/releases/download/v1.8.0/fabtests-1.8.0.tar.gz',
             sha256='4b9af18c9c7c8b28eaeac4e6e9148bd2ea7dc6b6f00f8e31c90a6fc536c5bb6c',
             placement='fabtests', when='@1.8.0')
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
             placement='fabtests', when='@1.4.2')

    def setup_build_environment(self, env):
        if self.run_tests:
            env.prepend_path('PATH', self.prefix.bin)

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

    def install(self, spec, prefix):
        # Call main install method
        super(Libfabric, self).install(spec, prefix)

        # Build and install fabtests, if available
        if not os.path.isdir('fabtests'):
            return
        with working_dir('fabtests'):
            configure = Executable('./configure')
            configure('--prefix={0}'.format(self.prefix),
                      '--with-libfabric={0}'.format(self.prefix))
            make()
            make('install')

    def installcheck(self):
        fi_info = Executable(self.prefix.bin.fi_info)
        fi_info()

        # Run fabtests test suite if available
        if not os.path.isdir('fabtests'):
            return
        if self.spec.satisfies('@1.8.0,1.9.0'):
            # make test seems broken.
            return
        with working_dir('fabtests'):
            make('test')
