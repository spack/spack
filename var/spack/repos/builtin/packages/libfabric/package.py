# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libfabric(AutotoolsPackage):
    """The Open Fabrics Interfaces (OFI) is a framework focused on exporting
       fabric communication services to applications."""

    homepage = "https://libfabric.org/"
    url      = "https://github.com/ofiwg/libfabric/releases/download/v1.8.0/libfabric-1.8.0.tar.bz2"
    git      = "https://github.com/ofiwg/libfabric.git"

    maintainers = ['rajachan']

    version('master', branch='master')
    version('1.14.1', sha256='6cfabb94bca8e419d9015212506f5a367d077c5b11e94b9f57997ec6ca3d8aed')
    version('1.14.0', sha256='fc261388848f3cff555bd653f5cb901f6b9485ad285e5c53328b13f0e69f749a')
    version('1.13.2', sha256='25d783b0722a8df8fe61c1de75fafca684c5fe520303180f26f0ad6409cfc0b9')
    version('1.13.1', sha256='8e6eed38c4a39aa4cbf7d5d3734f0eecbfc030182f1f9b3be470702f2586d30e')
    version('1.12.1', sha256='db3c8e0a495e6e9da6a7436adab905468aedfbd4579ee3da5232a5c111ba642c')
    version('1.12.0', sha256='ca98785fe25e68a26c61e272be64a1efeea37e61b0dcebd34ccfd381bda7d9cc')
    version('1.11.2', sha256='ff2ba821b55a54855d327e6f6fb8a14312c9c9ca7c873525b6a246d8f974d7da')
    version('1.11.1', sha256='a72a7dac6322bed09ef1af33bcade3024ca5847a1e9c8fa369da6ab879111fe7')
    version('1.11.0', sha256='9938abf628e7ea8dcf60a94a4b62d499fbc0dbc6733478b6db2e6a373c80d58f')
    version('1.10.1', sha256='889fa8c99eed1ff2a5fd6faf6d5222f2cf38476b24f3b764f2cbb5900fee8284')
    version('1.10.0', sha256='c1ef6e9cd6dafec3f003d2f78f0f3a25f055a7a791e98b5a0db1e4c5036e40f6')
    version('1.9.1', sha256='c305c6035c992523e08c7591a6a3707225ba3e72de40443eaed837a10df6771a')
    version('1.9.0', sha256='559bfb7376c38253c936d0b104591c3394880376d676894895706c4f5f88597c')
    version('1.8.1', sha256='3c560b997f9eafd89f961dd8e8a29a81aad3e39aee888e3f3822da419047dc88')
    version('1.8.0', sha256='c4763383a96af4af52cd81b3b094227f5cf8e91662f861670965994539b7ee37')
    version('1.7.1', sha256='f4e9cc48319763cff4943de96bf527b737c9f1d6ac3088b8b5c75d07bd719569')
    version('1.7.0', sha256='b3dd9cc0fa36fe8c3b9997ba279ec831a905704816c25fe3c4c09fc7eeceaac4')
    version('1.6.2', sha256='ec63f61f5e529964ef65fd101627d8782c0efc2b88b3d5fc7f0bfd2c1e95ab2c')
    version('1.6.1', sha256='33215a91450e2234ebdc7c467f041b6757f76f5ba926425e89d80c27b3fd7da2')
    version('1.6.0', sha256='b3ce7bd655052ea4da7bf01a3177d96d94e5f41b3fd6011ac43f50fcb2dc7581')
    version('1.5.3', sha256='f62a40da06f8951db267a59a4ee7363b6ee60a7abbc55cd5db6c8b067d93fa0c')
    version('1.5.0', sha256='88a8ad6772f11d83e5b6f7152a908ffcb237af273a74a1bd1cb4202f577f1f23')
    version('1.4.2', sha256='5d027d7e4e34cb62508803e51d6bd2f477932ad68948996429df2bfff37ca2a5')

    fabrics = ('efa',
               'gni',
               'mlx',
               'mrail',
               'psm',
               'psm2',
               'psm3',
               'rxm',
               'rxd',
               'shm',
               'sockets',
               'tcp',
               'udp',
               'usnic',
               'verbs',
               'xpmem')

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

    variant('debug', default=False,
            description='Enable debugging')

    # For version 1.9.0:
    # headers: fix forward-declaration of enum fi_collective_op with C++
    patch('https://github.com/ofiwg/libfabric/commit/2e95b0efd85fa8a3d814128e34ec57ffd357460e.patch?full_index=1',
          sha256='456693e28bb1fc41a0bbb94b97ae054e7d28f81ca94795d7f294243da58c6376',
          when='@1.9.0')

    # Fix for the inline assembly problem for the Nvidia compilers
    # https://github.com/ofiwg/libfabric/pull/7665
    patch('nvhpc-symver.patch', when='@1.6.0:1.14.0 %nvhpc')

    depends_on('rdma-core', when='fabrics=verbs')
    depends_on('opa-psm2', when='fabrics=psm2')
    depends_on('psm', when='fabrics=psm')
    depends_on('ucx', when='fabrics=mlx')

    depends_on('m4', when='@develop', type='build')
    depends_on('autoconf', when='@develop', type='build')
    depends_on('automake', when='@develop', type='build')
    depends_on('libtool', when='@develop', type='build')

    conflicts('@1.9.0', when='platform=darwin',
              msg='This distribution is missing critical files')

    def setup_build_environment(self, env):
        if self.run_tests:
            env.prepend_path('PATH', self.prefix.bin)

    @when('@develop')
    def autoreconf(self, spec, prefix):
        bash = which('bash')
        bash('./autogen.sh')

    def configure_args(self):
        args = []

        args.extend(self.enable_or_disable('debug'))

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
