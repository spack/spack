# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Astra(Package):
    """A Space Charge Tracking Algorithm."""

    homepage = "http://www.desy.de/~mpyflo/"

    version('2016-11-30', sha256='50738bf924724e2dd15f1d924b290ffb0f7c703e5d5ae02ffee2db554338801e', expand=False,
            url='http://www.desy.de/~mpyflo/Astra_for_64_Bit_Linux/Astra')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('Astra', prefix.bin)

        chmod = which('chmod')
        chmod('+x', join_path(prefix.bin, 'Astra'))
