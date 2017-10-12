##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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


class KaksCalculator(MakefilePackage):
    """KaKs_Calculator adopts model selection and model averaging to calculate
       nonsynonymous (Ka) and synonymous (Ks) substitution rates, attempting to
       include as many features as needed for accurately capturing evolutionary
       information in protein-coding sequences."""

    homepage = "https://code.google.com/archive/p/kaks-calculator/"
    url      = "https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/kaks-calculator/KaKs_Calculator1.2.tar.gz"

    version('1.2', '4f89bf211a5a32adaf38a76ef63b46fd')

    def url_for_version(self, version):
        url = 'https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/kaks-calculator/KaKs_Calculator{0}.tar.gz'
        return url.format(version)

    build_directory = 'src'

    # include<string.h> needs added to header file for compilation to work
    def patch(self):
        with working_dir(self.build_directory):
            header = FileFilter('base.h')
            header.filter('#include<time.h>',
                          '#include<time.h>\n#include<string.h>')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir(self.build_directory):
            install('KaKs_Calculator', prefix.bin)
            install('ConPairs', prefix.bin)
            install('AXTConvertor', prefix.bin)
        install_tree('doc', prefix.doc)
        install_tree('examples', prefix.examples)
