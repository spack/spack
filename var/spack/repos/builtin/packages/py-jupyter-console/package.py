# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJupyterConsole(PythonPackage):
    """Jupyter Terminal Console"""

    homepage = "https://github.com/jupyter/jupyter_console"
    url      = "https://github.com/jupyter/jupyter_console/archive/5.0.0.tar.gz"

    version('5.2.0', 'a783ec26193b2835caa94e255e05e080')
    version('5.0.0', '08a9fde32a45c9e2e0b4cec6eca249c2')
    version('4.1.1', 'a8b077ae0a5c57e9518ac039ad5febb8')
    version('4.1.0', '9c655076262760bdbeeada9d7f586237')
    version('4.0.3', '0e928ea261e7f8154698cf69ed4f2459')
    version('4.0.2', 'f2e174938c91136549b908bd39fa5d59')

    depends_on('python@2.7:2.8,3.3:')
    depends_on('py-jupyter-client', type=('build', 'run'))
    depends_on('py-ipython', type=('build', 'run'))
    depends_on('py-ipykernel', type=('build', 'run'))
    depends_on('py-pygments', type=('build', 'run'))
