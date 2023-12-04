# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAstrovascpy(PythonPackage):
    """
    Vasculature blood flow computation and impact of astrocytic
    endfeet on vessels
    """

    homepage = "https://github.com/BlueBrain/AstroVascPy"
    git = "https://github.com/BlueBrain/AstroVascPy.git"

    maintainers("tristan0x")

    version("0.1.2", tag="0.1.2")

    variant("vtk", default=False, description="add VTK support (mainly for visualization)")

    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-setuptools-scm", type="build")

    depends_on("py-click", type=("build", "run"))
    depends_on("py-cached-property", type=("build", "run"))
    depends_on("py-coverage", type=("build", "run"))
    depends_on("py-cython", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-libsonata", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-morphio", type=("build", "run"))
    depends_on("py-networkx", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-petsc4py", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-seaborn", type=("build", "run"))
    depends_on("py-tables", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-trimesh", type=("build", "run"))
    depends_on("py-vascpy", type=("build", "run"))
    depends_on("vtk+python", type=("build", "run"), when="+vtk")

    depends_on("py-pytest", type="test")
    depends_on("py-pytest-mpi", type="test")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def test_install(self):
        python("-m", "pytest", "tests")
