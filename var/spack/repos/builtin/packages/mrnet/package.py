# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mrnet(AutotoolsPackage):
    """The MRNet Multi-Cast Reduction Network."""

    homepage = "http://paradyn.org/mrnet"
    url      = "http://ftp.cs.wisc.edu/pub/paradyn/mrnet/mrnet_5.0.1.tar.gz"
    git      = "https://github.com/dyninst/mrnet.git"
    list_url = "http://ftp.cs.wisc.edu/paradyn/mrnet"

    version('5.0.1-3', branch='master')
    version('5.0.1-2', commit='20b1eacfc6d680d9f6472146d2dfaa0f900cc2e9')
    version('5.0.1', '17f65738cf1b9f9b95647ff85f69ecdd')
    version('4.1.0', '5a248298b395b329e2371bf25366115c')
    version('4.0.0', 'd00301c078cba57ef68613be32ceea2f')

    variant('cti', default=False,
            description="Build the MRNet with the CTI startup option")
    variant('lwthreads', default=False,
            description="Also build the MRNet LW threadsafe libraries")
    parallel = False

    depends_on("boost")
    depends_on("cti", when='+cti')

    def configure_args(self):
        spec = self.spec
        config_args = ['--enable-shared']

        # Build the MRNet LW thread safe libraries when the
        # lwthreads variant is present
        if '+lwthreads' in spec:
            config_args.append('--enable-ltwt-threadsafe')
        # Build the MRNet with CTI based start-up when
        # the cti variant is present
        if '+cti' in spec:
            config_args.append('--with-startup=cray-cti')
            cti = self.spec['cti'].prefix
            config_args.append('--with-craycti-inc=-I%s/include' % cti)
            config_args.append('--with-craycti-lib=-I%s/lib' % cti)
        return config_args
