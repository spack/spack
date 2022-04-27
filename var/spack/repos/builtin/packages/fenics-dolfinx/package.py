# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FenicsDolfinx(CMakePackage):
    """Next generation FEniCS problem solving environment"""

    homepage = "https://github.com/FEniCS/dolfinx"
    git = "https://github.com/FEniCS/dolfinx.git"
    url = "https://github.com/FEniCS/dolfinx/archive/v0.1.0.tar.gz"
    maintainers = ["chrisrichardson", "garth-wells", "nate-sime"]

    version("main", branch="main")
    version("0.4.0", sha256="2c9b36b97c22d9bbe7b9b57f0e4d9693d42d778ea0d21321926db7ca66dd338d")
    version("0.3.0", sha256="4857d0fcb44a4e9bf9eb298ba5377abdee17a7ad0327448bdd06cce73d109bed")
    version("0.2.0", sha256="4c9b5a5c7ef33882c99299c9b4d98469fb7aa470a37a91bc5be3bb2fc5b863a4")
    version("0.1.0", sha256="0269379769b5b6d4d1864ded64402ecaea08054c2a5793c8685ea15a59af5e33")

    variant("kahip", default=False, description="kahip support")
    variant("parmetis", default=False, description="parmetis support")
    variant("slepc", default=False, description="slepc support")
    variant("adios2", default=False, description="adios2 support")

    depends_on("cmake@3.18:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("mpi")
    depends_on("hdf5+mpi")
    depends_on("boost@1.7.0:+filesystem+program_options+timer")

    depends_on("petsc+mpi+shared")
    depends_on("petsc+mpi+shared@3.15.0:", when="@0.1.0")
    depends_on("scotch+mpi")
    depends_on("xtensor@0.23.10:", type=("build", "link"))

    depends_on("kahip", when="+kahip")
    depends_on("parmetis", when="+parmetis")
    depends_on("slepc", when="+slepc")
    depends_on("adios2", when="+adios2")

    depends_on("fenics-ufcx@main", type=("build", "run"), when="@main")
    depends_on("fenics-ufcx@0.4.0", type=("build", "link"), when="@0.4.0")

    # depends_on("py-fenics-ffcx", type=("build", "run"))
    # depends_on("py-fenics-ffcx@main", type=("build", "run"), when="@main")
    # depends_on("py-fenics-ffcx@0.4.0", type=("build", "run"), when="@0.4.0")
    depends_on("py-fenics-ffcx@0.3.0", type=("build", "run"), when="@0.3.0")
    depends_on("py-fenics-ffcx@0.2.0", type=("build", "run"), when="@0.2.0")
    depends_on("py-fenics-ffcx@0.1.0", type=("build", "run"), when="@0.1.0")

    depends_on("fenics-basix", type=("build", "link"))
    depends_on("fenics-basix@main", type=("build", "link"), when="@main")
    depends_on("fenics-basix@0.4.0", type=("build", "link"), when="@0.4.0")
    depends_on("fenics-basix@0.3.0", type=("build", "link"), when="@0.3.0")
    depends_on("fenics-basix@0.2.0", type=("build", "link"), when="@0.2.0")
    depends_on("fenics-basix@0.1.0", type=("build", "link"), when="@0.1.0")

    conflicts('%gcc@:8', msg='Improved C++17 support required')

    root_cmakelists_dir = "cpp"

    @when('@0.4.0:')
    def cmake_args(self):
        args = [
            "-DDOLFINX_SKIP_BUILD_TESTS=True",
            "-DDOLFINX_ENABLE_KAHIP=%s" % (
                'ON' if "+kahip" in self.spec else 'OFF'),
            "-DDOLFINX_ENABLE_PARMETIS=%s" % (
                'ON' if "+parmetis" in self.spec else 'OFF'),
            "-DDOLFINX_ENABLE_SLEPC=%s" % (
                'ON' if "+slepc" in self.spec else 'OFF'),
            "-DDOLFINX_ENABLE_ADIOS2=%s" % (
                'ON' if "+adios2" in self.spec else 'OFF'),
        ]
        return args

    @when('@:0.3.0')
    def cmake_args(self):
        args = [
            "-DDOLFINX_SKIP_BUILD_TESTS=True",
            "-DDOLFINX_ENABLE_KAHIP=%s" % (
                'ON' if "+kahip" in self.spec else 'OFF'),
            "-DDOLFINX_ENABLE_PARMETIS=%s" % (
                'ON' if "+parmetis" in self.spec else 'OFF'),
            "-DDOLFINX_ENABLE_SLEPC=%s" % (
                'ON' if "+slepc" in self.spec else 'OFF'),
            "-DDOLFINX_ENABLE_ADIOS2=%s" % (
                'ON' if "+adios2" in self.spec else 'OFF'),
            "-DPython3_ROOT_DIR=%s" % self.spec['python'].home,
            "-DPython3_FIND_STRATEGY=LOCATION",
        ]
        return args
          # args.append("-DPython3_ROOT_DIR=%s" % self.spec['python'].home)
          # args.append("-DPython3_FIND_STRATEGY=LOCATION")
