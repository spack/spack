# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class OpaPsm2(MakefilePackage):
    """ Intel Omni-Path Performance Scaled Messaging 2 (PSM2) library"""

    homepage = "http://github.com/intel/opa-psm2"
    url      = "https://github.com/intel/opa-psm2/archive/PSM2_10.3-8.tar.gz"

    version('11.2.77', sha256='5cc33d1e19d871a5861efe0bb897526f404b4bf2b88ac58bb277db96ac5ecb54')
    version('11.2.68', sha256='42e16a14fc8c90b50855dcea46af3315bee32fb1ae89d83060f9b2ebdce1ec26')
    version('10.3-37',  '9bfca04f29b937b3856f893e1f8b1b60')
    version('10.3-17',  'e7263eb449939cb87612e2c7623ca21c')
    version('10.3-10',  '59d36b49eb126f980f3272a9d66a8e98')
    version('10.3-8',   '07bc5cb2a6bf1189a29cbea836843db2')
    version('10.2-260', '71df31b5776be64ff243417ac88eec66')
    version('10.2-235', '23539f725a597bf2d35aac47a793a37b')
    version('10.2-175', 'c542b8641ad573f08f61d0a6a70f4013')

    variant('avx2', default=True, description='Enable AVX2 instructions')

    depends_on('numactl')

    # patch to prevent opa-psm2 from adding an additional "usr/"
    #   subdirectory within the installation prefix, which breaks paths for
    #   dependent packages like libfabric
    patch('opa-psm2-install-prefix.patch', when='@11.2.68:')

    # patch to get the Makefile to use the spack compiler wrappers
    patch('opa-psm2-compiler.patch', when='@11.2.68:',
          sha256='fe31fda9aaee13acb87d178af2282446196d2cc0b21163034573706110b2e2d6')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('DESTDIR', self.prefix)
        if '%intel' in self.spec:
            # this variable must be set when we use the Intel compilers to
            # ensure that the proper flags are set
            spack_env.set('CCARCH', 'icc')

    def edit(self, spec, prefix):
        # Change the makefile so libraries and includes are not
        # placed under $PREFIX/usr
        env['LIBDIR'] = '/lib'
        filter_file(r'${DESTDIR}/usr', '${DESTDIR}', 'Makefile')

        if '~avx2' in spec:
            env['PSM_DISABLE_AVX2'] = 'True'

    def install(self, spec, prefix):
        make('--environment-overrides', 'install')
