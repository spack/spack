##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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


class Openmc(CMakePackage):
    """The OpenMC project aims to provide a fully-featured Monte Carlo particle
       transport code based on modern methods. It is a constructive solid
       geometry, continuous-energy transport code that uses ACE format cross
       sections. The project started under the Computational Reactor Physics
       Group at MIT."""

    homepage = "http://openmc.readthedocs.io/"
    url = "https://github.com/mit-crpg/openmc/tarball/v0.10.0"

    version('0.10.0', 'abb57bd1b226eb96909dafeec31369b0')
    version('develop', git='https://github.com/mit-crpg/openmc.git')

    depends_on("hdf5+hl")

    def cmake_args(self):
        options = ['-DHDF5_ROOT:PATH=%s' % self.spec['hdf5'].prefix]

        return options
