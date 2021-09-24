# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNbclassic(PythonPackage):
    """Jupyter Notebook as a Jupyter Server Extension."""

    homepage = "https://github.com/jupyterlab/nbclassic"
    pypi     = "nbclassic/nbclassic-0.3.1.tar.gz"

    version('0.3.1', sha256='f920f8d09849bea7950e1017ff3bd101763a8d68f565a51ce053572e65aa7947')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-jupyter-server@1.8:1.999', type=('build', 'run'))
    depends_on('py-notebook@:6.999', type=('build', 'run'))
