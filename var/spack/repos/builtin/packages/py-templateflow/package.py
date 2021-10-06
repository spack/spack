# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTemplateflow(PythonPackage):
    """A python client to query TemplateFlow via pyBIDS."""

    homepage = "https://github.com/templateflow/python-client"
    pypi     = "templateflow/templateflow-0.7.1.tar.gz"

    version('0.7.1', sha256='c6e8282d1ffbb5dca7bd704a12e02bd00021860b71a043c35716861910c7187f')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools@40.9:', type='build')
    depends_on('py-setuptools-scm+toml@3.4:', type='build')
    depends_on('py-wheel', type='build')
    depends_on('py-pybids@0.12.1:', type=('build', 'run'))
    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-tqdm', type=('build', 'run'))
