# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import shutil

from spack.pkgkit import *


class Ucx(AutotoolsPackage, CudaPackage):
    """a communication library implementing high-performance messaging for
    MPI/PGAS frameworks"""

    homepage = "http://www.openucx.org"
    url      = "https://github.com/openucx/ucx/releases/download/v1.3.1/ucx-1.3.1.tar.gz"
    git      = "https://github.com/openucx/ucx.git"

    maintainers = ['hppritcha']

    # Current
    version('1.12.1', sha256='40b447c8e7da94a253f2828001b2d76021eb4ad39647107d433d62d61e18ae8e')
    version('1.12.0', sha256='93e994de2d1a4df32381ea92ba4c98a249010d1720eb0f6110dc72c9a7d25db6')
    version('1.11.2', sha256='deebf86a5344fc2bd9e55449f88c650c4514928592807c9bc6fe4190e516c6df')
    version('1.11.1', sha256='29338cad18858517f96b46ff83bdd259a5899e274792cebd269717c660aa86fd')
    version('1.11.0', sha256='b7189b69fe0e16e3c03784ef674e45687a9c520750bd74a45125c460ede37647')
    version('1.10.1', sha256='ae9a108af6842ca135e7ec9b6131469adf9f1e50f899349fafcc69a215368bc9')
    version('1.10.0', sha256='b885e24b1b94724c03cb213c355381e98df1e2d1fd7f633cf8055b6dd05db92d')
    version('1.9-dev', branch='v1.9.x')
    version('1.9.0', sha256='a7a2c8841dc0d5444088a4373dc9b9cc68dbffcd917c1eba92ca8ed8e5e635fb')
    version('1.8.1', sha256='a48820cb8d0761b5ccf3e7ba03a7c8c1dde6276017657178829e07ffc35b556a')
    version('1.8.0', sha256='e400f7aa5354971c8f5ac6b881dc2846143851df868088c37d432c076445628d')
    version('1.7.0', sha256='6ab81ee187bfd554fe7e549da93a11bfac420df87d99ee61ffab7bb19bdd3371')
    version('1.6.1', sha256='1425648aa03f5fa40e4bc5c4a5a83fe0292e2fe44f6054352fbebbf6d8f342a1')
    version('1.6.0', sha256='360e885dd7f706a19b673035a3477397d100a02eb618371697c7f3ee4e143e2c')
    version('1.5.2', sha256='1a333853069860e86ba69b8d071ccc9871209603790e2b673ec61f8086913fad')
    version('1.5.1', sha256='567119cd80ad2ae6968ecaa4bd1d2a80afadd037ccc988740f668de10d2fdb7e')
    version('1.5.0', sha256='84f6e4fa5740afebb9b1c8bb405c07206e58c56f83120dcfcd8dc89e4b7d7458')
    version('1.4.0', sha256='99891a98476bcadc6ac4ef9c9f083bc6ffb188a96b3c3bc89c8bbca64de2c76e')

    # Still supported
    version('1.3.1', sha256='e058c8ec830d2f50d9db1e3aaaee105cd2ad6c1e6df20ae58b9b4179de7a8992')
    version('1.3.0', sha256='71e69e6d78a4950cc5a1edcbe59bf7a8f8e38d59c9f823109853927c4d442952')
    version('1.2.2', sha256='914d10fee8f970d4fb286079dd656cf8a260ec7d724d5f751b3109ed32a6da63')
    version('1.2.1', sha256='fc63760601c03ff60a2531ec3c6637e98f5b743576eb410f245839c84a0ad617')
    version('1.2.0', sha256='1e1a62d6d0f89ce59e384b0b5b30b416b8fd8d7cedec4182a5319d0dfddf649c')

    simd_values = ('avx', 'sse41', 'sse42')

    variant('thread_multiple', default=False,
            description='Enable thread support in UCP and UCT')
    variant('optimizations', default=True,
            description='Enable optimizations')
    variant('logging', default=False,
            description='Enable logging')
    variant('debug', default=False,
            description='Enable debugging')
    variant('opt', default='3', values=('0', '1', '2', '3'), multi=False,
            description='Set optimization level')
    variant('assertions', default=False,
            description='Enable assertions')
    variant('parameter_checking', default=False,
            description='Enable parameter checking')
    variant('pic', default=True,
            description='Builds with PIC support')
    variant('java', default=False,
            description='Builds with Java bindings')
    variant('gdrcopy', default=False,
            description='Enable gdrcopy support')
    variant('knem', default=False,
            description='Enable KNEM support')
    variant('xpmem', default=False,
            description='Enable XPMEM support')
    variant('cma', default=False,
            description="Enable Cross Memory Attach")
    variant('rocm', default=False,
            description="Enable ROCm support")
    variant('rc', default=False,
            description="Compile with IB Reliable Connection support")
    variant('dc', default=False,
            description="Compile with IB Dynamic Connection support")
    variant('ud', default=False,
            description="Compile with IB Unreliable Datagram support")
    variant('mlx5-dv', default=False,
            description="Compile with mlx5 Direct Verbs support")
    variant('ib-hw-tm', default=False,
            description="Compile with IB Tag Matching support")
    variant('dm', default=False,
            description="Compile with Device Memory support")
    variant('cm', default=False, when='@:1.10',
            description="Compile with IB Connection Manager support")
    variant('backtrace-detail', default=False,
            description="Enable using BFD support for detailed backtrace")
    variant('openmp', default=True,
            description="Use OpenMP")
    variant('shared', default=True,
            description="Build shared libraries")
    variant('static', default=False,
            description="Build static libraries")
    variant('ucg', default=False,
            description="Enable the group collective operations " +
                        "(experimental component)")
    variant('doc', default=True,
            description="Generate doxygen documentation")
    variant('simd', values=disjoint_sets(
        ('auto',),
        simd_values).with_default('auto').with_non_feature_values('auto'))
    variant('verbs', default=False,
            description='Build OpenFabrics support')
    variant('rdmacm', default=False,
            description='Enable the use of RDMACM')
    variant('examples', default=True,
            description='Keep examples')

    depends_on('numactl')
    depends_on('rdma-core', when='+verbs')
    depends_on('rdma-core', when='+rdmacm')
    depends_on('pkgconfig', type='build')
    depends_on('java@8', when='+java')
    depends_on('maven', when='+java')
    depends_on('gdrcopy', when='@1.7:+gdrcopy')
    depends_on('gdrcopy@1.3', when='@:1.6+gdrcopy')
    conflicts('+gdrcopy', when='~cuda',
              msg='gdrcopy currently requires cuda support')
    conflicts('+rocm', when='+gdrcopy',
              msg='gdrcopy > 2.0 does not support rocm')
    depends_on('xpmem', when='+xpmem')
    depends_on('knem', when='+knem')
    depends_on('binutils+ld', when='%aocc', type='build')
    depends_on('binutils+ld', when='+backtrace-detail')

    conflicts('~shared', when='~static', msg='Please select at least one of +static or +shared')

    configure_abs_path = 'contrib/configure-release'

    @when('@1.9-dev')
    def autoreconf(self, spec, prefix):
        Executable('./autogen.sh')()

    def configure_args(self):
        spec = self.spec
        config_args = []

        if '+thread_multiple' in spec:
            config_args.append('--enable-mt')
        else:
            config_args.append('--disable-mt')

        if '+cma' in spec:
            config_args.append('--enable-cma')
        else:
            config_args.append('--disable-cma')

        if '+paramter_checking' in spec:
            config_args.append('--enable-params-check')
        else:
            config_args.append('--disable-params-check')

        rdmac_prefix = lambda x: self.spec['rdma-core'].prefix \
            if 'rdma-core' in self.spec else None

        config_args.extend(self.enable_or_disable('optimizations'))
        config_args.append('--enable-compiler-opt=' +
                           self.spec.variants['opt'].value)
        config_args.extend(self.enable_or_disable('assertions'))
        config_args.extend(self.enable_or_disable('logging'))

        config_args.extend(self.enable_or_disable('backtrace-detail'))
        config_args.extend(self.with_or_without('pic'))
        config_args.extend(self.with_or_without('rc'))
        config_args.extend(self.with_or_without('ud'))
        config_args.extend(self.with_or_without('dc'))
        config_args.extend(self.with_or_without('mlx5-dv'))
        config_args.extend(self.with_or_without('ib-hw-tm'))
        config_args.extend(self.with_or_without('dm'))
        config_args.extend(self.with_or_without('cm'))
        config_args.extend(self.with_or_without('rocm'))
        config_args.extend(self.with_or_without('java',
                                                activation_value='prefix'))
        config_args.extend(self.with_or_without('cuda',
                                                activation_value='prefix'))
        config_args.extend(self.with_or_without('gdrcopy',
                                                activation_value='prefix'))
        config_args.extend(self.with_or_without('knem',
                                                activation_value='prefix'))
        config_args.extend(self.with_or_without('xpmem',
                                                activation_value='prefix'))
        config_args.extend(self.with_or_without('rdmacm',
                                                activation_value=rdmac_prefix))

        config_args.extend(self.enable_or_disable('static'))
        config_args.extend(self.enable_or_disable('shared'))
        config_args.extend(self.enable_or_disable('static'))
        config_args.extend(self.with_or_without('openmp'))

        if self.spec.satisfies('simd=auto'):
            # Activate SIMD based on properties of the target
            if 'avx' in self.spec.target:
                config_args.append('--with-avx')
            else:
                config_args.append('--without-avx')
        elif self.spec.satisfies('simd=none'):
            for instr in self.simd_values:
                config_args.append('--without-' + instr)
        else:
            for instr in self.simd_values:
                if self.spec.satisfies('simd=' + instr):
                    config_args.append('--with-' + instr)
                else:
                    config_args.append('--without-' + instr)

        config_args.extend(self.with_or_without('verbs',
                                                activation_value=rdmac_prefix))

        # lld doesn't support '-dynamic-list-data'
        if '%aocc' in spec:
            config_args.append('LDFLAGS=-fuse-ld=bfd')

        return config_args

    @run_after('install')
    def drop_examples(self):
        if self.spec.satisfies('~examples'):
            shutil.rmtree(join_path(self.spec.prefix, 'share', 'ucx', 'examples'))
