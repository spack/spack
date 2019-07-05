# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJupyterhub(PythonPackage):
    """Multi-user server for Jupyter notebooks."""

    homepage = "https://pypi.org/project/jupyterhub"
    url      = "https://pypi.io/packages/source/j/jupyterhub/jupyterhub-0.9.4.tar.gz"

    version('0.9.4',    sha256='86b1cce446d4e8347e26913878858fc8964d103fde19b606fe37ccc5188d629d')

    depends_on('python@3.5:')
    depends_on('node-js', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-python-dateutil', type='run')
    depends_on('py-jinja2', type='run')
    depends_on('py-sqlalchemy', type='run')
    depends_on('py-tornado', type='run')
    depends_on('py-traitlets', type='run')
    depends_on('py-alembic', type='run')
    depends_on('py-mako', type='run')
    depends_on('py-async-generator', type='run')
    depends_on('py-jupyter-notebook', type='run')
    depends_on('py-prometheus-client', type='run')
    depends_on('py-send2trash', type='run')
    depends_on('py-requests', type='run')
