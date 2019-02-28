# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libbeagle(AutotoolsPackage, CudaPackage):
    """Beagle performs genotype calling, genotype phasing, imputation of
       ungenotyped markers, and identity-by-descent segment detection."""

    homepage = "https://github.com/beagle-dev/beagle-lib"
    url      = "https://github.com/beagle-dev/beagle-lib/archive/beagle_release_2_1_2.tar.gz"

    version('2.1.2', '1107614e86f652f8ee45c1c92f2af3d4')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    depends_on('subversion', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('java', type='build')

    def patch(self):
        # update cuda architecture if necessary
        if '+cuda' in self.spec:
            arch = self.spec.variants['cuda_arch'].value
            archflag = ''

            if arch[0] != 'none':
                archflag = '-arch=%s' % arch[0]

            filter_file('-arch compute_13', archflag,
                        'libhmsbeagle/GPU/kernels/Makefile.am',
                        string=True)

            # point CUDA_LIBS to libcuda.so
            filter_file('-L$with_cuda/lib', '-L$with_cuda/lib64/stubs',
                        'configure.ac', string=True)

    def configure_args(self):
        args = []

        if '+cuda' in self.spec:
            args.append('--with-cuda=%s' % spec['cuda'].prefix)
        else:
            args.append('--without-cuda')

        return args

    def url_for_version(self, version):
        url = "https://github.com/beagle-dev/beagle-lib/archive/beagle_release_{0}.tar.gz"
        return url.format(version.underscored)

    def setup_environment(self, spack_env, run_env):
        prefix = self.prefix
        run_env.prepend_path('BEAST_LIB', prefix.lib)
