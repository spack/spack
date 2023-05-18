# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Celeritas(CMakePackage, CudaPackage, ROCmPackage):
    """Celeritas is a new Monte Carlo transport code designed for
    high-performance (GPU-targeted) simulation of high-energy physics
    detectors.
    """

    homepage = "https://github.com/celeritas-project/celeritas"
    url = "https://github.com/celeritas-project/celeritas/releases/download/v0.1.0/celeritas-0.1.0.tar.gz"

    maintainers("sethrj")

    version("0.2.1", sha256="b3717b43f70dd0da848139da4171ca7a887bb6777908845b6d953d47b1f4db41")
    version(
        "0.2.0",
        sha256="12af28fda0e482a9eba89781b4ead445cf6f170bc1b8d88cc814e49b1ec09e9f",
        deprecated=True,
    )
    version("0.1.5", sha256="5e63b9ce7fcfe34a8938565b84453bce51fa6639d1ede13bb59d41de6431cef4")
    version(
        "0.1.4",
        sha256="ea82a03fc750a2a805f87afd9ac944109dd7537edb5c0c370f93d332d4cd47db",
        deprecated=True,
    )
    version(
        "0.1.3",
        sha256="992c49a48adba884fe3933c9624da5bf480ef0694809430ae98903f2c28cc881",
        deprecated=True,
    )
    version(
        "0.1.2",
        sha256="d123ea2e34267adba387d46bae8c9a1146a2e047f87f2ea5f823878c1684678d",
        deprecated=True,
    )
    version(
        "0.1.1",
        sha256="a1d58e29226e89a2330d69c40049d61e7c885cf991824e60ff8c9ccc95fc5ec6",
        deprecated=True,
    )
    version(
        "0.1.0",
        sha256="46692977b9b31d73662252cc122d7f016f94139475788bca7fdcb97279b93af8",
        deprecated=True,
    )

    _cxxstd_values = ("14", "17")

    # Note: cuda and rocm variants are defined by mixin classes
    variant(
        "cxxstd",
        default="17",
        values=_cxxstd_values,
        multi=False,
        description="C++ standard version",
    )
    variant("debug", default=False, description="Enable runtime debug assertions")
    variant("doc", default=False, description="Build and install documentation")
    variant("geant4", default=True, description="Use Geant4 data")
    variant("hepmc3", default=True, description="Use HepMC3 I/O interfaces")
    variant("openmp", default=False, description="Use OpenMP multithreading")
    variant("root", default=False, description="Use ROOT I/O")
    variant("shared", default=True, description="Build shared libraries")
    variant("swig", default=False, description="Generate SWIG Python bindings")
    variant("vecgeom", default=True, description="Use VecGeom geometry")

    depends_on("cmake@3.13:", type="build")
    depends_on("cmake@3.18:", type="build", when="+cuda+vecgeom")
    depends_on("cmake@3.22:", type="build", when="+rocm")

    depends_on("nlohmann-json")
    depends_on("geant4@10.7:11.0", when="@:0.2.0 +geant4")
    depends_on("geant4@10.6:11.0", when="@0.2.1: +geant4")
    depends_on("hepmc3", when="+hepmc3")
    depends_on("root", when="+root")
    depends_on("swig", when="+swig")
    depends_on("vecgeom", when="+vecgeom")

    depends_on("python", type="build")
    depends_on("doxygen", type="build", when="+doc")
    depends_on("py-breathe", type="build", when="+doc")
    depends_on("py-sphinx", type="build", when="+doc")

    for _std in _cxxstd_values:
        depends_on("geant4 cxxstd=" + _std, when="+geant4 cxxstd=" + _std)
        depends_on("root cxxstd=" + _std, when="+root cxxstd=" + _std)
        depends_on("vecgeom cxxstd=" + _std, when="+vecgeom cxxstd=" + _std)

    depends_on("vecgeom +gdml@1.1.17:", when="+vecgeom")
    depends_on("vecgeom +cuda", when="+vecgeom +cuda")

    conflicts("cxxstd=14", when="@0.3:")
    conflicts("+rocm", when="+cuda", msg="AMD and NVIDIA accelerators are incompatible")
    conflicts("+rocm", when="+vecgeom", msg="HIP support is only available with ORANGE")
    conflicts("^vecgeom+shared@1.2.0", when="+vecgeom +cuda")

    def cmake_args(self):
        define = self.define
        from_variant = self.define_from_variant
        args = [
            from_variant("BUILD_SHARED_LIBS", "shared"),
            from_variant("CELERITAS_DEBUG", "debug"),
            from_variant("CELERITAS_BUILD_DOCS", "doc"),
            define("CELERITAS_BUILD_DEMOS", False),
            define("CELERITAS_BUILD_TESTS", False),
            from_variant("Celeritas_USE_HIP", "rocm"),
            define("CELERITAS_USE_MPI", False),
            define("CELERITAS_USE_JSON", True),
            define("CELERITAS_USE_Python", True),
        ]

        for pkg in ["CUDA", "Geant4", "HepMC3", "OpenMP", "ROOT", "SWIG", "VecGeom"]:
            args.append(from_variant("CELERITAS_USE_" + pkg, pkg.lower()))

        return args
