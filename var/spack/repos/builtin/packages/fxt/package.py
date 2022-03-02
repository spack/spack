# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import subprocess


class Fxt(AutotoolsPackage):
    """This library provides efficient support for recording traces"""
    homepage = "http://savannah.nongnu.org/projects/fkt"

    maintainers = ['nfurmento', 'sthibaul']

    version('0.3.14', '317d8d93175cd9f27ec43b8390b6d29dc66114f06aa74f2329847d49baaaebf2',
            url="http://download.savannah.nongnu.org/releases/fkt/fxt-0.3.14.tar.gz")
    version('0.3.5', '6d5ad611be66576a1f1a6a6ca9a8ad42',
            url="http://download.savannah.nongnu.org/releases/fkt/fxt-0.3.5.tar.gz")
    version('0.3.4', '1c1c1cb8087a1e009a5fcf3a42583c3d',
            url="http://download.savannah.nongnu.org/releases/fkt/fxt-0.3.4.tar.gz")
    version('0.3.3', '52055550a21655a30f0381e618081776',
            url="http://download.savannah.nongnu.org/releases/fkt/fxt-0.3.3.tar.gz")

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
