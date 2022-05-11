# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterServer(PythonPackage):
    """The Jupyter Server provides the backend (i.e. the core services, APIs,
    and REST endpoints) for Jupyter web applications like Jupyter notebook,
    JupyterLab, and Voila."""

    homepage = "https://github.com/jupyter-server/jupyter_server"
    pypi     = "jupyter_server/jupyter_server-1.9.0.tar.gz"

    version('1.13.5', sha256='9e3e9717eea3bffab8cfb2ff330011be6c8bbd9cdae5b71cef169fcece2f19d3')
    version('1.11.2', sha256='c1f32e0c1807ab2de37bf70af97a36b4436db0bc8af3124632b1f4441038bf95')
    version('1.11.1', sha256='ab7ab1cc38512f15026cbcbb96300fb46ec8b24aa162263d9edd00e0a749b1e8')
    version('1.11.0', sha256='8ab4f484a4a2698f757cff0769d27b5d991e0232a666d54f4d6ada4e6a61330b')
    version('1.10.2', sha256='d3a3b68ebc6d7bfee1097f1712cf7709ee39c92379da2cc08724515bb85e72bf')
    version('1.9.0', sha256='7d19006380f6217458a9db309b54e3dab87ced6c06329c61823907bef2a6f51b')
    version('1.6.1', sha256='242ddd0b644f10e030f917019b47c381e0f2d2b950164af45cbd791d572198ac')

    depends_on('python@3.7:', when='@1.13.2:', type=('build', 'run'))
    depends_on('python@3.6:', type=('build', 'run'))
    # TODO: replace this after concretizer learns how to concretize separate build deps
    depends_on('py-jupyter-packaging11', when='@1.6.2:', type='build')
    # depends_on('py-jupyter-packaging@0.9:0', when='@1.6.2:', type='build')
    depends_on('py-setuptools', type='build')
    depends_on('py-jinja2', type=('build', 'run'))
    depends_on('py-tornado@6.1:', type=('build', 'run'))
    depends_on('py-pyzmq@17:', type=('build', 'run'))
    depends_on('py-argon2-cffi', type=('build', 'run'))
    depends_on('py-ipython-genutils', type=('build', 'run'))
    depends_on('py-traitlets@5:', when='@1.13.3:', type=('build', 'run'))
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
    depends_on('py-packaging', when='@1.13.2:', type=('build', 'run'))
    # for windows depends_on pywinpty@:1, when='@1.13.2:'
    depends_on('py-requests-unixsocket', when='@:1.11.1', type=('build', 'run'))
