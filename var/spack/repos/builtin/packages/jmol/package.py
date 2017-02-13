##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
from distutils.dir_util import copy_tree


class Jmol(Package):
    """Jmol: an open-source Java viewer for chemical structures in 3D
    with features for chemicals, crystals, materials and biomolecules."""

    homepage = "http://jmol.sourceforge.net/"
    url      = "https://sourceforge.net/projects/jmol/files/Jmol/Version%2014.8/Jmol%2014.8.0/Jmol-14.8.0-binary.tar.gz"

    version('14.8.0', '3c9f4004b9e617ea3ea0b78ab32397ea')

    depends_on('jdk', type='run')

    def install(self, spec, prefix):
        copy_tree('jmol-{0}'.format(self.version), prefix)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', self.prefix)
        run_env.set('JMOL_HOME', self.prefix)
