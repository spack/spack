# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PipGlibc(Package):
    """Glibc for PiP"""

    homepage = "https://github.com/RIKEN-SysSoft/PiP-glibc"
    git      = "https://github.com/RIKEN-SysSoft/PiP-glibc.git"

    version('1', branch='centos/glibc-2.17-260.el7.pip.branch')

    def install(self, spec, prefix):
        bash = which('bash')
        with working_dir('PiP-glibc.build', create=True):
            bash('../build.sh', '%s' % prefix)
