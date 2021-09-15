# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gnuconfig(Package):
    """
    The GNU config.guess and config.sub scripts versioned by timestamp.
    This package can be used as a build dependency for autotools packages that
    ship a tarball with outdated config.guess and config.sub files.
    """

    homepage = "https://www.gnu.org/software/config/"
    git      = "https://github.com/haampie/config.git"
    url      = "https://github.com/haampie/config/archive/refs/tags/2021-08-14.tar.gz"

    maintainers = ['haampie']

    version('master', branch='master')
    version('2021-08-14', sha256='1d1134f2f9d5f1342693793a536643c9aa11eaf672d1bf453ce2a415fdb8ebcc')

    def install(self, spec, prefix):
        with working_dir(self.stage.source_path):
            install('config.sub', prefix)
            install('config.guess', prefix)
