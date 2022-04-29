# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class Gnuconfig(Package):
    """
    The GNU config.guess and config.sub scripts versioned by timestamp.
    This package can be used as a build dependency for autotools packages that
    ship a tarball with outdated config.guess and config.sub files.
    """

    homepage = "https://www.gnu.org/software/config/"
    git      = "https://github.com/spack/gnuconfig.git"
    url      = "https://github.com/spack/gnuconfig/releases/download/2021-08-14/gnuconfig-2021-08-14.tar.gz"

    maintainers = ['haampie']

    version('master', branch='master')
    version('2021-08-14', sha256='69b6d2868e70167ba1bdb9030b49beeb20f00b37e30825e83fd04291d96bc5f7')

    def install(self, spec, prefix):
        with working_dir(self.stage.source_path):
            install('config.sub', prefix)
            install('config.guess', prefix)
