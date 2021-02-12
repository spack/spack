# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyStdlibList(PythonPackage):
    """This package includes lists of all of the standard libraries
    for Python, along with the code for scraping the official Python
    docs to get said lists."""

    pypi = "stdlib-list/stdlib-list-0.6.0.tar.gz"

    version('0.8.0', sha256='a1e503719720d71e2ed70ed809b385c60cd3fb555ba7ec046b96360d30b16d9f')
    version('0.7.0', sha256='66c1c1724a12667cdb35be9f43181c3e6646c194e631efaaa93c1f2c2c7a1f7f')
    version('0.6.0', sha256='133cc99104f5a4e1604dc88ebb393529bd4c2b99ae7e10d46c0b596f3c67c3f0')

    depends_on('py-functools32', when="^python@:3.1", type=('build', 'run'))
    depends_on('py-setuptools', type='build')
