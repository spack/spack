# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFenicsDolfinx(PythonPackage):
    """Python interface library to Next generation FEniCS problem solving
    environment"""

    homepage = "https://github.com/FEniCS/dolfinx"
    url = "https://github.com/FEniCS/dolfinx/archive/v0.1.0.tar.gz"
    git = "https://github.com/FEniCS/dolfinx.git"
    maintainers = ["chrisrichardson", "garth-wells", "nate-sime"]

    version("main", branch="main")
    version("0.3.0", sha256="4857d0fcb44a4e9bf9eb298ba5377abdee17a7ad0327448bdd06cce73d109bed")
    version("0.2.0", sha256="4c9b5a5c7ef33882c99299c9b4d98469fb7aa470a37a91bc5be3bb2fc5b863a4")
    version("0.1.0", sha256="0269379769b5b6d4d1864ded64402ecaea08054c2a5793c8685ea15a59af5e33")

    depends_on("cmake@3.18:", type="build")
    depends_on("hdf5", type="build")
    depends_on("pkgconfig", type=("build", "run"))
    depends_on('python@3.7:', type=('build', 'run'))
    depends_on("py-setuptools", type="build")
    depends_on("fenics-dolfinx@main", when="@main")
    depends_on("fenics-dolfinx@0.3.0", when="@0.3.0")
    depends_on("fenics-dolfinx@0.2.0", when="@0.2.0")
    depends_on("fenics-dolfinx@0.1.0", when="@0.1.0")
    depends_on("fenics-basix@main", type=("build", "link"), when="@main")
    depends_on("fenics-basix@0.3.0", type=("build", "link"), when="@0.3.0")
    depends_on("fenics-basix@0.2.0", type=("build", "link"), when="@0.2.0")
    depends_on("fenics-basix@0.1.0", type=("build", "link"), when="@0.1.0")
    depends_on("py-numpy@:1.20.3", type=("build", "run"))
    depends_on("py-mpi4py", type=("build", "run"))
    depends_on("py-petsc4py", type=("build", "run"))
    depends_on("py-pybind11@2.6.2:2.7", type=("build", "run"))
    depends_on("xtensor@0.23.10:", type="build")

    depends_on("py-fenics-ffcx@main", type="run", when="@main")
    depends_on("py-fenics-ffcx@0.3.0", type="run", when="@0.3.0")
    depends_on("py-fenics-ffcx@0.2.0", type="run", when="@0.2.0")
    depends_on("py-fenics-ffcx@0.1.0", type="run", when="@0.1.0")
    depends_on("py-fenics-ufl@main", type="run", when="@main")
    depends_on("py-fenics-ufl@2021.1.0", type="run", when="@0.1:0.3.99")

    depends_on("py-cffi", type="run")
    depends_on("py-numpy", type="run")

    phases = ['build_ext', 'build', 'install']

    build_directory = 'python'
