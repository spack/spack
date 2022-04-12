# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyOpenmesh(PythonPackage):
    """A versatile halfedge-based data structure for representing and
    manipulating polygon meshes"""

    homepage = "https://www.graphics.rwth-aachen.de:9000/OpenMesh/openmesh-python"
    url = "https://pypi.io/packages/source/o/openmesh/openmesh-1.1.3.tar.gz"

    version('1.1.3', sha256='c1d24abc85b7b518fe619639f89750bf19ed3b8938fed4dd739a72f1e6f8b0f6', preferred=True)

    depends_on('cmake@3.1:', type='build')
    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')
    depends_on('py-pip', type='build')

    depends_on('py-numpy', type=('build', 'run'))
