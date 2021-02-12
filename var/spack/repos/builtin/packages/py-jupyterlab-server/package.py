# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyJupyterlabServer(PythonPackage):
    """A set of server components for JupyterLab and JupyterLab
       like applications"""

    pypi = "jupyterlab_server/jupyterlab_server-1.2.0.tar.gz"

    version('2.2.0', sha256='68b9322eee2561c89a22fcdf755c57fd750e8132f18fda81d47ca336d1f9b066')
    version('2.1.5', sha256='eab98f9159bde9b329dfe5828bdbab5415e3562f14188a05696b8292c481c6b3')
    version('2.1.4', sha256='688dee616ab89a9d5313f89da99c48abd10433a2c18a327c6e4d2b4c51707753')
    version('2.1.3', sha256='2af96b04bacf49a17bd2abdd461a219ab62724c39aea2d39ba95ded4be9a171a')
    version('2.1.2', sha256='a71ebeb89eb2ab49eca41768f9840bb6896c264203ea755990313d4dfa610a74')
    version('2.1.1', sha256='67bfd4acfef24cf94e3dc0971cf6fa0eee13cc84ee47cdcd704257a0975b22ad')
    version('2.1.0', sha256='990e59bef1b7545c1adb4aacbdde441f1ff29fea017b117c7a383039f31ec92d')
    version('2.0.0', sha256='1350c36954d3d16c71129b30b60b9df11e8fcf2f3acf88596f6abc8a79b0c918')
    version('1.2.0', sha256='5431d9dde96659364b7cc877693d5d21e7b80cea7ae3959ecc2b87518e5f5d8c')
    version('1.1.0', sha256='bac27e2ea40f686e592d6429877e7d46947ea76c08c878081b028c2c89f71733')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-json5', type=('build', 'run'))
    depends_on('py-jsonschema@3.0.1:', type=('build', 'run'))
    depends_on('py-notebook@4.2.0:', type=('build', 'run'))
    depends_on('py-jinja2@2.10:', type=('build', 'run'))
