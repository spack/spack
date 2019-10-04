# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJupyterhub(PythonPackage):
    """Multi-user server for Jupyter notebooks."""

    homepage = "https://pypi.org/project/jupyterhub"
    url      = "https://pypi.io/packages/source/j/jupyterhub/jupyterhub-1.0.0.tar.gz"

    version('1.0.0',    sha256='33541a515a041b9a518ca057c1c4ab4215a7450fdddc206401713ee8137fa67f')

    depends_on('python@3.5:')
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
