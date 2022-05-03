# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Tamaas(SConsPackage):
    """
    Tamaas is a C++ library with a Python interface to efficiently solve
    contact mechanics problems with periodic rough surfaces, plasticity,
    adhesion and friction.
    """

    homepage = "https://gitlab.com/tamaas/tamaas"
    url      = "https://gitlab.com/tamaas/tamaas/-/archive/v2.4.0/tamaas-v2.4.0.tar.gz"
    git      = "https://gitlab.com/tamaas/tamaas.git"
    maintainers = ["prs513rosewood"]

    version("master", branch="master")
    version("2.4.0", sha256="38edba588ff3a6643523c28fb391e001dbafa9d0e58053b9e080eda70f8c71c9")
    version("2.3.1", sha256="7d63e374cbc7b5b93578ece7be5c084d1c2f0dbe1d57c4f0c8abd5ff5fff9ab0")
    version("2.3.0", sha256="0529e015c6cb5bbabaea5dce6efc5ec0f2aa76c00541f0d90ad0e2e3060a4520")

    variant("python", default=True,
            description="Provide Python bindings for Tamaas")
    variant("solvers", default=True, when="+python",
            description="Enables extra Scipy-based nonlinear solvers")

    depends_on("scons@3:", type="build")
    depends_on("thrust", type="build")
    depends_on("boost", type="build")
    depends_on("fftw-api@3:")

    # compilers that don't use C++14 by default cause configure issues
    conflicts("%gcc@:5")
    conflicts("%clang@:5")
    conflicts("%intel")

    with when("+python"):
        extends("python")
        # Python 3.6 causes unicode issues with scons
        depends_on("python@3.7:", type=("build", "run"))
        depends_on("py-numpy", type=("build", "run"))
        depends_on("py-scipy", when="+solvers", type="run")
        depends_on("py-pybind11", type="build")
        depends_on("py-wheel", type="build")

    def build_args(self, spec, prefix):
        args = [
            "build_type=release",
            "use_mpi={}".format(spec["fftw-api"].satisfies("+mpi")),
            "backend={}".format(
                "omp" if spec["fftw-api"].satisfies("+openmp") else "cpp"),
            "fftw_threads={}".format(
                "omp" if spec["fftw-api"].satisfies("+openmp") else "none"),
            "build_python={}".format(spec.satisfies("+python")),
            "verbose=True",
            "strip_info=True",
            "real_type=double",
            "integer_type=int",
            "build_tests=False",
            "prefix={}".format(prefix),
            "BOOST_ROOT={}".format(spec['boost'].prefix),
            "THRUST_ROOT={}".format(spec['thrust'].prefix),
            "FFTW_ROOT={}".format(spec['fftw-api'].prefix),
        ]

        if spec.satisfies("+python"):
            args += [
                "PYBIND11_ROOT={}".format(spec['py-pybind11'].prefix),
            ]

        return args
