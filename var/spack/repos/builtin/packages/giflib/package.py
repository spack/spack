# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Giflib(MakefilePackage, SourceforgePackage):
    """The GIFLIB project maintains the giflib service library, which has
    been pulling images out of GIFs since 1989."""

    homepage = "http://giflib.sourceforge.net/"
    sourceforge_mirror_path = "giflib/giflib-5.1.4.tar.gz"

    version('5.2.1', sha256='31da5562f44c5f15d63340a09a4fd62b48c45620cd302f77a6d9acf0077879bd')
    version('5.2.0', sha256='dc7257487c767137602d86c17098ec97065a718ff568a61cfcf1a9466f197b1f')
    version('5.1.4', sha256='df27ec3ff24671f80b29e6ab1c4971059c14ac3db95406884fc26574631ba8d5', extension='tar.bz2')

    depends_on('automake', type='build', when='@:5.2.0')
    depends_on('autoconf', type='build', when='@:5.2.0')
    depends_on('m4', type='build', when='@:5.2.0')
    depends_on('libtool', type='build', when='@:5.2.0')

    patch('bsd-head.patch')

    @property
    def install_targets(self):
        targets = ['install']
        if self.spec.satisfies('@5.2.0:'):
            targets.append('PREFIX={0}'.format(self.spec.prefix))
            targets.append('LIBMAJOR={0}'.format(self.spec.version.up_to(1)))
            targets.append('LIBVER={0}'.format(self.spec.version))

        return targets

    def check(self):
        make('check', parallel=False)

    def edit(self, spec, prefix):
        if spec.satisfies('@:5.2.0'):
            configure = Executable('./configure')
            configure('--prefix={0}'.format(prefix))
