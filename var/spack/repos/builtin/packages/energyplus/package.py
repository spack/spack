# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob
import os


class Energyplus(Package):
    """EnergyPlus is a whole building energy simulation program that engineers,
       architects, and researchers use to model both energy consumption for
       heating, cooling, ventilation, lighting and plug and process loads
       and water use in buildings"""

    homepage = "https://energyplus.net"

    # versions require explicit URLs as they contain hashes
    version('8.9.0', sha256='13a5192b25815eb37b3ffd019ce3b99fd9f854935f8cc4362814f41c56e9ca98',
            url="https://github.com/NREL/EnergyPlus/releases/download/v8.9.0-WithIDDFixes/EnergyPlus-8.9.0-eba93e8e1b-Linux-x86_64.tar.gz")

    def install(self, spec, prefix):
        # binary distribution, we just unpack to lib/energyplus
        # and then symlink the appropriate targets

        # there is only one folder with a semi-predictable name so we glob it
        install_tree(glob.glob('EnergyPlus*')[0],
                     join_path(prefix.lib, 'energyplus'))

        mkdirp(prefix.bin)
        os.symlink(join_path(prefix.lib, 'energyplus/energyplus'),
                   join_path(prefix.bin, 'energyplus'))
        os.symlink(join_path(prefix.lib, 'energyplus/EPMacro'),
                   join_path(prefix.bin, 'EPMacro'))
        os.symlink(join_path(prefix.lib, 'energyplus/ExpandObjects'),
                   join_path(prefix.bin, 'ExpandObjects'))
