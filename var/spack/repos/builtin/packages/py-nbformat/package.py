# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNbformat(PythonPackage):
    """The Jupyter Notebook format"""

    homepage = "https://github.com/jupyter/nbformat"
    url      = "https://github.com/jupyter/nbformat/archive/4.1.0.tar.gz"

    version('4.1.0', '826b4fc4ec42553b20144f53b57b4e7b')
    version('4.0.1', 'ab7172e517c9d561c0c01eef5631b4c8')
    version('4.0.0', '7cf61359fa4e9cf3ef5e969e2fcb909e')

    depends_on('py-ipython-genutils', type=('build', 'run'))
    depends_on('py-traitlets', type=('build', 'run'))
    depends_on('py-jsonschema', type=('build', 'run'))
    depends_on('py-jupyter-core', type=('build', 'run'))
