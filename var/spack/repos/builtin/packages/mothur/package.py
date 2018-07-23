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


class Mothur(MakefilePackage):
    """This project seeks to develop a single piece of open-source, expandable
       software to fill the bioinformatics needs of the microbial ecology
       community."""

    homepage = "https://github.com/mothur/mothur"
    url      = "https://github.com/mothur/mothur/archive/v1.39.5.tar.gz"

    version('1.40.5', 'd57847849fdb961c3f66c9b9fdf3057b')
    version('1.39.5', '1f826ea4420e6822fc0db002c5940b92')

    depends_on('boost')
    depends_on('readline')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        makefile.filter('BOOST_LIBRARY_DIR=\"\\\"Enter_your_boost_library_path'
                        '_here\\\"\"', 'BOOST_LIBRARY_DIR=%s' %
                        self.spec['boost'].prefix.lib)
        makefile.filter('BOOST_INCLUDE_DIR=\"\\\"Enter_your_boost_include_path'
                        '_here\\\"\"', 'BOOST_INCLUDE_DIR=%s' %
                        self.spec['boost'].prefix.include)
        makefile.filter('MOTHUR_FILES=\"\\\"Enter_your_default_path_'
                        'here\\\"\"', 'MOTHUR_FILES=%s' % prefix)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('mothur', prefix.bin)
        install('uchime', prefix.bin)
        install_tree('source', prefix.include)
