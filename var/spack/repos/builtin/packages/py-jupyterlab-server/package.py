# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.pkgkit import *


class PyJupyterlabServer(PythonPackage):
    """A set of server components for JupyterLab and JupyterLab
       like applications"""

    homepage = "https://github.com/jupyterlab/jupyterlab_server"
    pypi = "jupyterlab_server/jupyterlab_server-1.2.0.tar.gz"

    version('2.10.3', sha256='3fb84a5813d6d836ceda773fb2d4e9ef3c7944dbc1b45a8d59d98641a80de80a')
    version('2.6.0', sha256='f300adf6bb0a952bebe9c807a3b2a345d62da39b476b4f69ea0dc6b5f3f6b97d')
    version('1.2.0', sha256='5431d9dde96659364b7cc877693d5d21e7b80cea7ae3959ecc2b87518e5f5d8c')
    version('1.1.0', sha256='bac27e2ea40f686e592d6429877e7d46947ea76c08c878081b028c2c89f71733')

    depends_on('python@3.6:', when='@2.5:', type=('build', 'run'))
    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    # TODO: replace this after concretizer learns how to concretize separate build deps
    depends_on('py-jupyter-packaging11', type='build')
    # depends_on('py-jupyter-packaging@0.9:0', type='build')

    depends_on('py-babel', when='@2.5.1:', type=('build', 'run'))
    depends_on('py-entrypoints@0.2.2:', when='@2.7:', type=('build', 'run'))
    depends_on('py-jinja2@2.10:', type=('build', 'run'))
    depends_on('py-json5', type=('build', 'run'))
    depends_on('py-jsonschema@3.0.1:', type=('build', 'run'))
    depends_on('py-packaging', when='@2.5.1:', type=('build', 'run'))
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-jupyter-server@1.4:1', when='@2.5.1:', type=('build', 'run'))
    depends_on('py-notebook@4.2.0:', when='@:2.5.0', type=('build', 'run'))
