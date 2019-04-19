# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Udocker(Package):
    """A basic user tool to execute simple docker containers in batch or
    interactive systems without root privileges.

    https://doi.org/10.1016/j.cpc.2018.05.021"""

    homepage = "https://github.com/indigo-dc/udocker"
    git      = "https://github.com/indigo-dc/udocker.git"

    version('1.1.3', tag='v1.1.3')

    def install(self, spec, prefix):
        # udocker consists of a single python script
        source = 'udocker.py'
        dest = join_path(prefix.bin, 'udocker')

        mkdir(prefix.bin)
        install(source, dest)

        chmod = which('chmod')
        chmod('a+x', dest)
