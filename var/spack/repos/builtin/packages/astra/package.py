# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Astra(Package):
    """A Space Charge Tracking Algorithm."""

    homepage = "http://www.desy.de/~mpyflo/"

    version('2016-11-30', '17135b7a4adbacc1843a50a6a2ae2c25', expand=False,
            url='http://www.desy.de/~mpyflo/Astra_for_64_Bit_Linux/Astra')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('Astra', prefix.bin)

        chmod = which('chmod')
        chmod('+x', join_path(prefix.bin, 'Astra'))
