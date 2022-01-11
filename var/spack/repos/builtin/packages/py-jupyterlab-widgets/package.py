# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJupyterlabWidgets(PythonPackage):
    """A JupyterLab extension."""

    homepage = "https://github.com/jupyter-widgets/ipywidgets"
    pypi     = "jupyterlab_widgets/jupyterlab_widgets-1.0.2.tar.gz"

    version('1.0.2', sha256='7885092b2b96bf189c3a705cc3c412a4472ec5e8382d0b47219a66cccae73cfa')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools@40.8.0:', type='build')
    depends_on('py-jupyter-packaging@0.7.9:0.7', type='build')
    depends_on('py-jupyterlab@3.0:3', type='build')
