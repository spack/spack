# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJupyterlab(PythonPackage):
    """JupyterLab is the next-generation web-based user interface
       for Project Jupyter."""

    homepage = "https://jupyterlab.readthedocs.io/"
    url      = "https://pypi.io/packages/source/j/jupyterlab/jupyterlab-2.1.0.tar.gz"

    version('2.1.0', sha256='8c239aababf5baa0b3d36e375fddeb9fd96f3a9a24a8cda098d6a414f5bbdc81')

    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    depends_on('py-notebook@4.3.1:', type=('build', 'run'))
    depends_on('py-tornado@6.0.3:', type=('build', 'run'))
    depends_on('py-jupyterlab-server@1.1.0:', type=('build', 'run'))
    depends_on('py-jinja2@2.10:', type=('build', 'run'))

    depends_on('py-pytest', type='test')
    depends_on('py-pytest-check-links', type='test')
    depends_on('py-requests', type='test')
    depends_on('py-wheel', type='test')
    depends_on('py-virtualenv', type='test')
