# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
