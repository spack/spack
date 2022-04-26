# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJupyterlabWidgets(PythonPackage):
    """A JupyterLab extension."""

    homepage = "https://github.com/jupyter-widgets/ipywidgets"
    # Source is also available, but I'm having issues getting it to build:
    # https://github.com/jupyter-widgets/ipywidgets/issues/3324
    url = "https://files.pythonhosted.org/packages/py3/j/jupyterlab_widgets/jupyterlab_widgets-1.0.2-py3-none-any.whl"

    version('1.1.0', sha256='c2a9bd3789f120f64d73268c066ed3b000c56bc1dda217be5cdc43e7b4ebad3f', expand=False)
    version('1.0.2', sha256='f5d9efface8ec62941173ba1cffb2edd0ecddc801c11ae2931e30b50492eb8f7', expand=False)

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools@40.8.0:', type='build')
    # TODO: replace this after concretizer learns how to concretize separate build deps
    depends_on('py-jupyter-packaging7', type='build')
    # depends_on('py-jupyter-packaging@0.7.9:0.7', type='build')
    depends_on('py-jupyterlab@3.0:3', type='build')
