# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
    url      = "https://github.com/schrodinger/pymol-open-source/archive/v2.3.0.tar.gz"

    version('2.3.0', sha256='62aa21fafd1db805c876f89466e47513809f8198395e1f00a5f5cc40d6f40ed0')

    depends_on('python+tkinter', type=('build', 'run'))
    depends_on('freetype', type=('build', 'run'))
    depends_on('glew')
    depends_on('glm')
    depends_on('freeglut', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('tcsh', type=('build', 'run'))
    depends_on('py-pyqt5', type=('build', 'run'))
    depends_on('py-pmw', type=('build', 'run'))

    depends_on('libmmtf-cpp', type=('build'))
    depends_on('msgpack-c', type=('build'))
