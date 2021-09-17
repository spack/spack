# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GosamContrib(AutotoolsPackage):
    """Additional libraries for GoSam MC generator"""

    homepage = "https://gosam.hepforge.org"
    url      = "https://gosam.hepforge.org/downloads/?f=gosam-contrib-2.0.tar.gz"

    tags = ['hep']

    version('2.0', sha256='c05beceea74324eb51c1049773095e2cb0c09c8c909093ee913d8b0da659048d')
    version('1.0', sha256='a29d4232d9190710246abc2ed97fdcd8790ce83580f56a360f3456b0377c40ec')

    variant('shared', default=False, description='Build shared libraries')
    variant('static', default=True, description='Build static libraries')
    variant('pic', default=False, description='Build position-independent code')

    conflicts('~shared', when='~static', msg='Please enable at least one of shared or static')
    conflicts('~static', when='~shared', msg='Please enable at least one of shared or static')

    def configure_args(self):
        args = []
        args += self.enable_or_disable('shared')
        args += self.enable_or_disable('static')

        if '+pic' in spec:
            args.extend([
                'CFLAGS={0}'.format(self.compiler.cc_pic_flag),
                'CXXFLAGS={0}'.format(self.compiler.cxx_pic_flag),
                'FFLAGS={0} -std=legacy'.format(self.compiler.f77_pic_flag)
            ])
        else:
            args += "FFLAGS=-std=legacy"

        return args
