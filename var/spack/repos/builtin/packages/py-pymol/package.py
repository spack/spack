# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPymol(PythonPackage):
    """PyMOL is a Python-enhanced molecular graphics tool. It excels at 3D
       visualization of proteins, small molecules, density, surfaces, and
       trajectories. It also includes molecular editing, ray tracing, and
       movies. Open Source PyMOL is free to everyone!"""

    homepage = "https://pymol.org"
    url      = "https://sourceforge.net/projects/pymol/files/pymol/2/pymol-v2.1.0.tar.bz2"

    version('2.1.0', 'ef2ab2ce11d65785ca3258b4e6982dfb')

    depends_on('python+tkinter', type=('build', 'run'))
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
    depends_on('py-pyqt4', type=('build', 'run'))
    depends_on('freeglut')
