# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Zfp(MakefilePackage):
    """zfp is an open source C/C++ library for high-fidelity, high-throughput
       lossy compression of floating-point and integer multi-dimensional
       arrays.
    """

    homepage = 'http://computing.llnl.gov/projects/floating-point-compression'
    url      = 'http://computing.llnl.gov/projects/floating-point-compression/download/zfp-0.5.2.tar.gz'

    version('0.5.4', sha256='768a05ed9bf10e54ac306f90b81dd17b0e7b13782f01823d7da4394fd2da8adb')
    version('0.5.2', '2f0a77aa34087219a6e10b8b7d031e77')
    version('0.5.1', '0ed7059a9b480635e0dd33745e213d17')
    version('0.5.0', '2ab29a852e65ad85aae38925c5003654')

    variant('bsws',
            default='64',
            values=('8', '16', '32', '64'),
            multi=False,
            description='Bit stream word size: use smaller for finer '
            'rate granularity. Use 8 for H5Z-ZFP filter.')

    variant('shared', default=True,
            description='Build shared versions of the library')

    def edit(self, spec, prefix):
        config_file = FileFilter('Config')
        config_file.filter(
            r'^\s*#\s*DEFS\s*\+=\s*-DBIT_STREAM_WORD_TYPE\s*=\s*uint8',
            'DEFS += -DBIT_STREAM_WORD_TYPE=uint%s' %
            spec.variants['bsws'].value)

    def build(self, spec, prefix):
        with working_dir('src'):
            if '~shared' in spec:
                make('static')
            else:
                make('shared')

    def install(self, spec, prefix):
        incdir = 'include' if spec.satisfies('@0.5.1:') else 'inc'

        # Note: ZFP package does not provide an install target
        mkdirp(prefix.lib)
        mkdirp(prefix.include)
        # Note: ZFP package builds .so files even on OSX
        if '~shared' in spec:
            install('lib/libzfp.a', prefix.lib)
        else:
            install('lib/libzfp.so', prefix.lib)
        install('%s/zfp.h' % incdir, prefix.include)
        install('%s/bitstream.h' % incdir, prefix.include)
        if spec.satisfies('@0.5.1:'):
            mkdirp('%s/zfp' % prefix.include)
            install('%s/zfp/system.h' % incdir, '%s/zfp' % prefix.include)
            install('%s/zfp/types.h' % incdir, '%s/zfp' % prefix.include)
        else:
            install('%s/types.h' % incdir, prefix.include)
            install('%s/system.h' % incdir, prefix.include)
