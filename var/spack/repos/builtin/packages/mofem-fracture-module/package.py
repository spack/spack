##############################################################################
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


class MofemFractureModule(Package):
    """mofem fracture module"""

    homepage = "http://mofem.eng.gla.ac.uk"
    url = "https://bitbucket.org/likask/mofem_um_fracture_mechanics"

    maintainers = ['likask']

    version('0.9.40',
        git='https://bitbucket.org/likask/mofem_um_fracture_mechanics',
        tag='v0.9.40')
    version('develop',
        git='https://bitbucket.org/likask/mofem_um_fracture_mechanics',
        branch='develop')

    extends('mofem-cephas')

    def install(self, spec, prefix):
        source = self.stage.source_path
        mkdirp(prefix.users_modules.fracture_mechanics)
        install_tree(source, prefix.users_modules.fracture_mechanics)

    phases = ['install']
