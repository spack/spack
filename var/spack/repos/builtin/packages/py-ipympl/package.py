# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIpympl(PythonPackage):
    """Matplotlib Jupyter Extension."""

    homepage = "https://github.com/matplotlib/ipympl"
    pypi     = "ipympl/ipympl-0.8.8.tar.gz"
    maintainers = ['haralmha']

    version('0.8.8', sha256='5bf5d780b07fafe7924922ac6b2f3abd22721f341e5e196b3b82737dfbd0e1c9')

    depends_on('py-setuptools@40.8:', type='build')
    depends_on('py-ipython@:8', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-ipython-genutils', type=('build', 'run'))
    depends_on('pil', type=('build', 'run'))
    depends_on('py-traitlets@:5', type=('build', 'run'))
    depends_on('py-ipywidgets@7.6:7', type=('build', 'run'))
    depends_on('py-matplotlib@2:3', type=('build', 'run'))
    # TODO: replace this after concretizer learns how to concretize separate build deps  
    depends_on('py-jupyter-packaging7', type='build')                                    
    # depends_on('py-jupyter-packaging@0.7', type='build')
    depends_on('py-jupyterlab@3', type='build')
    depends_on('yarn', type='build')
