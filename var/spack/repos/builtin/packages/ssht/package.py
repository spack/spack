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


class Ssht(Package):
    """The SSHT code provides functionality to perform fast and exact
    spin spherical harmonic transforms."""

    homepage = "https://astro-informatics.github.io/ssht/"
    git      = "https://github.com/astro-informatics/ssht.git"

    version('1.2b1', commit='7378ce8853897cbd1b08adebf7ec088c1e40f860')

    depends_on('fftw')

    def install(self, spec, prefix):
        make('default')
        install_tree('include/c', join_path(prefix, 'include'))
        install_tree('doc/c', join_path(prefix, 'doc'))
        install_tree('lib/c', join_path(prefix, 'lib'))
