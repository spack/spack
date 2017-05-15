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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install vmd
#
# You can edit this file again by typing:
#
#     spack edit vmd
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Vmd(Package):
    """VMD is designed for the visualization and analysis of biological
    systems such as proteins, nucleic acids, lipid bilayer assemblies,
    etc.  It may be used to view more general molecules, as VMD can read
    standard Protein Data Bank (PDB) files and display the contained
    structure.  VMD provides a wide variety of methods for rendering and
    coloring molecule.  VMD can be used to animate and analyze the trajectory
    of molecular dynamics (MD) simulations, and can interactively manipulate
    molecules being simulated on remote computers (Interactive MD)."""

    homepage = "https://www-s.ks.uiuc.edu/Research/vmd"
    url      = "https://www-s.ks.uiuc.edu/Research/vmd/vmd-1.9.3/files/final/vmd-1.9.3.src.tar.gz"

    version('1.9.3', '5706f88b9b77cc5fafda6fef3a82d6fa')

#    #depends_on('autoconf', type='build')
#    #depends_on('automake', type='build')
#    #depends_on('libtool', type='build')
#    #depends_on('m4', type='build')

    def install(self, spec, prefix):
        configure()
        make()
        make("install")
