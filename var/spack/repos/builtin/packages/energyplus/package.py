##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

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
