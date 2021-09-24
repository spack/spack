# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNbmake(PythonPackage):
    """Pytest plugin for testing notebooks."""

    homepage = "https://github.com/treebeardtech/nbmake"
    pypi     = "nbmake/nbmake-0.5.tar.gz"

    version('0.5', sha256='da9bf1bbc377c9d1d697f99952834017c39b4983e7e482a038dec705955a8ae9')

    depends_on('python@3.6.1:3.999', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-pygments@2.7.3:2.999', type=('build', 'run'))
    depends_on('py-ipykernel@5.4.0:5.999', type=('build', 'run'))
    depends_on('py-nbclient@0.3:0.999', type=('build', 'run'))
    depends_on('py-nbformat@5.0.8:5.999', type=('build', 'run'))
    depends_on('py-pathlib@1.0.1:1.999', when='^python@:3.3', type=('build', 'run'))
    depends_on('py-pydantic@1.7.2:1.999', type=('build', 'run'))
    depends_on('py-pytest@6.1.2:6.999', type=('build', 'run'))
