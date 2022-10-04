# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyUnyt(PythonPackage):
    """A package for handling numpy arrays with units.

    """
    homepage = "https://yt-project.org"
   pypi = "unyt/unyt-2.8.0.tar.gz"
    git      = "https://github.com/yt-project/unyt.git"

    maintainers = ['qobilidop', 'charmoniumq']

    version("main", branch="main")
    version("2.8.0", sha256="4fc95704cba4527604f21724d0d9845aea07831a6a2a3d1be9b9d18395e0c345")
    version("2.7.2", sha256="9ad36f890549d18ecb9926019e96c4d27d380e909895a89ac7f1fb168a451edd")

    depends_on('py-setuptools', type='build')
    depends_on('python@3.5:', type=('build', 'run'))
    depends_on("py-numpy@1.13.0:", type=('build', 'run'))
    depends_on("py-sympy@1.2:", type=('build', 'run'))
