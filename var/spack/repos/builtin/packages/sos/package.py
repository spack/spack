# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sos(AutotoolsPackage):
    """Sandia OpenSHMEM."""

    homepage = "https://github.com/Sandia-OpenSHMEM/SOS"
    url      = "https://github.com/Sandia-OpenSHMEM/SOS/archive/refs/tags/v1.5.0.zip"

    # notify when the package is updated.
    maintainers = ['rscohn2']

    version('1.5.0', sha256='02679da6085cca2919f900022c46bad48479690586cb4e7f971ec3a735bab4d4')
    version('1.4.5', sha256='42778ba3cedb632ac3fbbf8917f415a804f8ca3b67fb3da6d636e6c50c501906')

    variant('xpmem', default=False, description='Enable xpmem for transport')
    variant('ofi', default=True, description='Enable ofi for transport')
    variant('shr-atomics', default=False, description='Enable shared memory atomic operations')

    depends_on('autoconf',  type='build')
    depends_on('automake',  type='build')
    depends_on('libtool',   type='build')
    depends_on('m4',        type='build')

    depends_on('libfabric', type='link', when='+ofi')
    depends_on('xpmem',     type='link', when='+xpmem')

    # Enable use of the OSH wrappers outside of Spack by preventing
    # them from using the spack wrappers
    filter_compiler_wrappers(
        'oshcc', 'oshc++', 'oshcc', 'oshfort', relative_root='bin'
    )

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.setup_compiler_environment(env)

        # Enable the osh wrappers to use spack wrappers when inside spack
        # with env variables
        env.set('SHMEM_CC', spack_cc)
        env.set('SHMEM_CXX', spack_cxx)
        env.set('SHMEM_FC', spack_fc)

    def autoreconf(self, spec, prefix):
        bash = Executable('bash')
        bash('./autogen.sh')

    def configure_args(self):
        args = []
        args.extend(self.with_or_without('xpmem'))
        args.extend(self.with_or_without('ofi'))
        # This option is not compatiable with remote atomics
        args.extend(self.enable_or_disable('shr-atomics'))
        args.append('--enable-pmi-simple')
        return args
