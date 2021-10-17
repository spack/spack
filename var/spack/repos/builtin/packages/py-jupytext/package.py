# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyJupytext(PythonPackage):
    """Jupyter Notebooks as Markdown Documents, Julia, Python or R scripts """

    homepage = "https://github.com/mwouts/jupytext/"
    git      = "https://github.com/mwouts/jupytext/"
    pypi     = "jupytext/jupytext-1.13.0.tar.gz"

    maintainers = ['vvolkl']

    version('1.13.0', sha256='fb220af65d2bd32d01c779b0e935c4c2b71e3f5f2f01bf1bab10d5f23fe121d4')

    depends_on('py-setuptools', type='build')
    depends_on('py-nbformat', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-toml', type=('build', 'run'))
    depends_on('py-mdit-py-plugins', type=('build', 'run'))
    depends_on('py-markdown-it-py@1.0:1', type=('build', 'run'))
