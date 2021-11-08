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

    import_modules = ['jupyter_server', 'jupyter_server.services',
                      'jupyter_server.services.contents',
                      'jupyter_server.services.kernels',
                      'jupyter_server.services.config'
                      'jupyter_server.services.security',
                      'jupyter_server.services.sessions',
                      'jupyter_server.services.nbconvert',
                      'jupyter_server.services.api',
                      'jupyter_server.services.kernelspecs',
                      'jupyter_server.auth', 'jupyter_server.tests',
                      'jupyter_server.tests.services',
                      'jupyter_server.tests.services.contents',
                      'jupyter_server.tests.services.kernels',
                      'jupyter_server.tests.services.config',
                      'jupyter_server.tests.services.sessions',
                      'jupyter_server.tests.services.nbconvert',
                      'jupyter_server.tests.services.api',
                      'jupyter_server.tests.services.kernelspecs',
                      'jupyter_server.tests.auth',
                      'jupyter_server.tests.unix_sockets',
                      'jupyter_server.tests.extension',
                      'jupyter_server.tests.extension.mockextensions',
                      'jupyter_server.tests.nbconvert',
                      'jupyter_server.terminal', 'jupyter_server.i18n',
                      'jupyter_server.base', 'jupyter_server.gateway',
                      'jupyter_server.extension',
                      'jupyter_server.prometheus', 'jupyter_server.view',
                      'jupyter_server.nbconvert',
                      'jupyter_server.files', 'jupyter_server.kernelspecs']

    version('1.11.2', sha256='c1f32e0c1807ab2de37bf70af97a36b4436db0bc8af3124632b1f4441038bf95')
    version('1.11.1', sha256='ab7ab1cc38512f15026cbcbb96300fb46ec8b24aa162263d9edd00e0a749b1e8')
    version('1.11.0', sha256='8ab4f484a4a2698f757cff0769d27b5d991e0232a666d54f4d6ada4e6a61330b')
    version('1.10.2', sha256='d3a3b68ebc6d7bfee1097f1712cf7709ee39c92379da2cc08724515bb85e72bf')
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
    depends_on('py-anyio@3.1.0:3', type=('build', 'run'))
    depends_on('py-websocket-client', type=('build', 'run'))
    depends_on('py-requests-unixsocket', type=('build', 'run'), when='@:1.11.1')
    depends_on('py-jupyter-packaging@0.9:1', type=('build', 'run'), when='@1.10.2:')
