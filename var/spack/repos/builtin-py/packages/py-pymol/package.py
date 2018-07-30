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


class PyPymol(PythonPackage):
    """PyMOL is a Python-enhanced molecular graphics tool. It excels at 3D
       visualization of proteins, small molecules, density, surfaces, and
       trajectories. It also includes molecular editing, ray tracing, and
       movies. Open Source PyMOL is free to everyone!"""

    homepage = "https://pymol.org"
    url      = "https://sourceforge.net/projects/pymol/files/pymol/2/pymol-v2.1.0.tar.bz2"

    version('2.1.0', 'ef2ab2ce11d65785ca3258b4e6982dfb')

    depends_on('python+tk', type=('build', 'run'))
    depends_on('tcl')
    depends_on('tk')
    depends_on('py-pmw')
    depends_on('gl')
    depends_on('glu')
    depends_on('glew')
    depends_on('libpng')
    depends_on('freetype')
    depends_on('libxml2')
    depends_on('msgpack-c')
    depends_on('py-pyqt', type=('build', 'run'))
    depends_on('freeglut')
