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
    version('0.9.3',    sha256='52e56371701d0105f9d6f16fb689c4126b52a5b6e54d8cb87f3655187a883fa3')
    version('0.9.2',    sha256='ef86512a485050dd28df9b785cb9912cbbbf69a131a34da216753af93d095da7')
    version('0.9.1',    sha256='56256ad6368f884fc34d5b52eb15350604bafc1c7b3516ae03303133446de644')
    version('0.9.0rc1', sha256='96758b5270254011799389a2e0d52db0a9262c5f6bcd70563415cffa8cc07906')
    version('0.9.0b3',  sha256='50d835c61b9f6deb9e337dc9cd0920eef2928d3136cb58061e4ebc838fdf9dab')
    version('0.9.0b2',  sha256='fc32abff12a4e6c9a72d581ac69f2b7eaa88e416b899c64b4316ccf8253ccc1b')
    version('0.9.0b1',  sha256='dc66d0638cc8865ff6dea6ce60578c1ed0343b81e0b55375ce6a27b7f3b1f882')
    version('0.9.0',    sha256='222ba6e0be1ba7754e134173ba88045b1d517c7eedc68aca1d4b0824b1984492')
    version('0.8.1',    sha256='1a9fc8c996c02344db00c852744b74bff1f552392b5c213b503ae47525020646')

    depends_on('python@3.5:')
    depends_on('node-js', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-dateutil', type='run')
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
