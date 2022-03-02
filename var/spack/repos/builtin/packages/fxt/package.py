# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import subprocess


class Fxt(AutotoolsPackage):
    """This library provides efficient support for recording traces"""

    homepage = "http://savannah.nongnu.org/projects/fkt"
    url = "http://download.savannah.nongnu.org/releases/fkt/fxt-0.3.14.tar.gz"

    maintainers = ['nfurmento', 'sthibaul']

    version('0.3.14', sha256='317d8d93175cd9f27ec43b8390b6d29dc66114f06aa74f2329847d49baaaebf2')
    version('0.3.5', sha256='3c0b33c82a01c4fb710c53ee9fc2c803314beba6fb60c397e13e874811e34a22')
    version('0.3.4', sha256='fcd35a5278ac0f10eba12fed4fa436dce79559897fde5b8176d5eee9081970f7')
    version('0.3.3', sha256='3f6fea5211cc242a54496e6242365c99522a5039916789cdbe25a58d05d6a626')

    variant('moreparams', default=False, description='Increase the value of FXT_MAX_PARAMS (to allow longer task names).')

    depends_on("gawk", type='build')

    def patch(self):
        # Increase the value of FXT_MAX_PARAMS (to allow longer task names)
        if '+moreparams' in self.spec:
            filter_file('#define FXT_MAX_PARAMS.*',
                        '#define FXT_MAX_PARAMS 16', 'tools/fxt.h')

    def autoreconf(self, spec, prefix):
        if not os.path.isfile("./configure"):
            if os.path.isfile("./autogen.sh"):
                subprocess.call(['libtoolize', '--copy', '--force'], shell=False)
                subprocess.check_call("./autogen.sh")
            else:
                raise RuntimeError('Neither configure nor autogen.sh script exist.\
                FxT Cannot configure.')

    def configure_args(self):
        args = []
        CFLAGS = []
        if "CFLAGS" in os.environ:
            CFLAGS.append(os.environ['CFLAGS'])
        # We don't have shared libraries but we still want it to be
        # possible to use this library in shared builds
        CFLAGS.append(self.compiler.cc_pic_flag)
        args.append('CFLAGS=' + ' '.join(CFLAGS))
        return args

    def build(self, spec, prefix):
        make(parallel=False)

    def install(self, spec, prefix):
        make('install', parallel=False)
