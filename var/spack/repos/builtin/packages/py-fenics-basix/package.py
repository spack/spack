# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFenicsBasix(PythonPackage):
    """Python basis evaluation library for Next generation FEniCS problem solving
    environment"""

    homepage = "https://github.com/FEniCS/basix"
    git = "https://github.com/FEniCS/basix.git"
    maintainers = ["chrisrichardson", "mscroggs"]

    version("main", branch="main")

    depends_on("cmake@3.9:", type="build")
    depends_on("eigen@3.3.7:")
    depends_on("python@3.5:", type=('build', 'run'))
    depends_on("py-setuptools", type="build")
    depends_on("py-scikit-build", type="build")
    depends_on("py-pybind11", type="build")

    phases = ['build', 'install']
