##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class SofaC(MakefilePackage):
    "Standards of Fundamental Astronomy (SOFA) library for ANSI C."

    homepage = "http://www.iausofa.org/current_C.html"
    url      = "http://www.iausofa.org/2018_0130_C/sofa_c-20180130.tar.gz"

    version('20180130', '9d6903c7690e84a788b622fba6f10146')

    @property
    def build_directory(self):
        return join_path(self.version, 'c', 'src')

    def edit(self, spec, prefix):
        makefile = FileFilter(join_path(self.build_directory, 'makefile'))
        makefile.filter('CCOMPC = gcc', 'CCOMPC = {0}'.format(spack_cc))

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            mkdir(prefix.include)
            install('sofa.h', prefix.include)
            install('sofam.h', prefix.include)
            mkdir(prefix.lib)
            install('libsofa_c.a', prefix.lib)
