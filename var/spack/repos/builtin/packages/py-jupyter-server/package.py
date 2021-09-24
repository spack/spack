# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJupyterServer(PythonPackage):
    """The Jupyter Server provides the backend (i.e. the core services, APIs,
    and REST endpoints) for Jupyter web applications like Jupyter notebook,
    JupyterLab, and Voila."""

    homepage = "https://github.com/jupyter-server/jupyter_server"
    pypi     = "jupyter_server/jupyter_server-1.9.0.tar.gz"

    version('1.9.0', sha256='7d19006380f6217458a9db309b54e3dab87ced6c06329c61823907bef2a6f51b')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-jinja2', type=('build', 'run'))
    depends_on('py-tornado@6.1:', type=('build', 'run'))
    depends_on('py-pyzmq@17:', type=('build', 'run'))
    depends_on('py-argon2-cffi', type=('build', 'run'))
    depends_on('py-ipython-genutils', type=('build', 'run'))
    depends_on('py-traitlets@4.2.1:', type=('build', 'run'))
    depends_on('py-jupyter-core@4.6.0:', type=('build', 'run'))
    depends_on('py-jupyter-client@6.1.1:', type=('build', 'run'))
    depends_on('py-nbformat', type=('build', 'run'))
    depends_on('py-nbconvert', type=('build', 'run'))
    depends_on('py-send2trash', type=('build', 'run'))
    depends_on('py-terminado@0.8.3:', type=('build', 'run'))
    depends_on('py-prometheus-client', type=('build', 'run'))
    depends_on('py-anyio@3.1.0:3.99', type=('build', 'run'))
    depends_on('py-websocket-client', type=('build', 'run'))
    depends_on('py-requests-unixsocket', type=('build', 'run'))
