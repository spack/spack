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


class Kraken(Package):
    """Kraken is a system for assigning taxonomic labels to short DNA
       sequences, usually obtained through metagenomic studies."""

    homepage = "https://ccb.jhu.edu/software/kraken/"
    url      = "https://github.com/DerrickWood/kraken/archive/v1.0.tar.gz"

    version('1.0', 'e790d6b09662bbd810aa34517ef66586')

    depends_on('perl', type=('build', 'run'))
    # Does NOT support JELLYFISH 2.0. Ver 1.1.11 is the last version of
    # JELLYFISH 1.
    depends_on('jellyfish@1.1.11', when='@1.0')

    def install(self, spec, prefix):
        installer = Executable('./install_kraken.sh')
        installer(self.stage.source_path)
        mkdirp(prefix.bin)
        files = glob.iglob('*')
        for file in files:
            if os.path.isfile(file):
                install(file, prefix.bin)
