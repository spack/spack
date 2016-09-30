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


class Hepmc(Package):
    """The HepMC package is an object oriented, C++ event record for
       High Energy Physics Monte Carlo generators and simulation."""

    homepage = "http://hepmc.web.cern.ch/hepmc/"
    url      = "http://hepmc.web.cern.ch/hepmc/releases/hepmc2.06.09.tgz"

    version('2.06.09', 'c47627ced4255b40e731b8666848b087')
    version('2.06.08', 'a2e889114cafc4f60742029d69abd907')
    version('2.06.07', '11d7035dccb0650b331f51520c6172e7')
    version('2.06.06', '102e5503537a3ecd6ea6f466aa5bc4ae')
    version('2.06.05', '2a4a2a945adf26474b8bdccf4f881d9c')

    depends_on("cmake", type='build')

    def install(self, spec, prefix):
        build_directory = join_path(self.stage.path, 'spack-build')
        source_directory = self.stage.source_path
        options = [source_directory]
        options.append('-Dmomentum:STRING=GEV')
        options.append('-Dlength:STRING=MM')
        options.extend(std_cmake_args)

        with working_dir(build_directory, create=True):
            cmake(*options)
            make()
            make('install')
