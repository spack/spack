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


class Mira(AutotoolsPackage):
    """MIRA is a multi-pass DNA sequence data assembler/mapper for whole genome
       and EST/RNASeq projects."""

    homepage = "http://sourceforge.net/projects/mira-assembler/"
    url      = "https://downloads.sourceforge.net/project/mira-assembler/MIRA/stable/mira-4.0.2.tar.bz2"

    version('4.0.2', '1921b426910653a34a6dbb37346f28ea')

    depends_on('boost@1.46:')
    depends_on('expat@2.0.1:')
    depends_on('gperftools')

    conflicts('%gcc@6:', when='@:4.0.2')

    def patch(self):
        with working_dir(join_path('src', 'progs')):
            edit = FileFilter('quirks.C')
            edit.filter('#include <boost/filesystem.hpp>',
                        '#include <boost/filesystem.hpp>\n#include <iostream>')

    def configure_args(self):
        args = ['--with-boost=%s' % self.spec['boost'].prefix,
                '--with-expat=%s' % self.spec['expat'].prefix]
        return args
