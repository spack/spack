# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFiona(PythonPackage):
    """Alternative Python binding for OGR"""

    homepage = "http://toblerity.org/fiona/"
    url      = "https://github.com/Toblerity/Fiona/archive/1.7.12.tar.gz"

    version('1.7.12', 'a2269acf64d9c87482e5d67dae19501c')

    depends_on('python@2.7:')
    
    depends_on('py-cligj@0.4:', type=('build', 'run'))
    depends_on('py-six@1.7:', type=('build', 'run'))
    depends_on('py-munch', type=('build', 'run'))
    depends_on('py-ordereddict', type=('build', 'run'))
    depends_on('gdal', type=('build', 'run'))
    depends_on('py-click-plugins', type=('build', 'run'))
    
    depends_on('py-setuptools',     type='build')
    depends_on('py-cython@0.21.2:', type='build')
    depends_on('py-nose', type='build')
    depends_on('py-coverage', type='build')
    depends_on('py-pytest', type='build')
    depends_on('py-pytest-cov', type='build')
