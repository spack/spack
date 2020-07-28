# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDolfinx(PythonPackage):
    """Python interface library to Next generation FEniCS problem solving environment"""

    homepage = "https://github.com/FEniCS/dolfinx"
    url = "https://github.com/FEniCS/dolfinx/archive/master.zip"
    git = "https://github.com/FEniCS/dolfinx.git"

    version("master", branch="master")

    depends_on("cmake@3.9:", type="build")
    depends_on("dolfinx@master")
    depends_on("py-pybind11")
    depends_on("py-mpi4py")
    depends_on("py-petsc4py")
    depends_on("py-scipy")

    root_cmakelists_dir = "cpp"

    import_modules = ['dolfinx']

    @property
    def build_directory(self):
        return join_path(self.stage.source_path, 'python')

