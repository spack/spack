# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.rocm import ROCmPackage

from spack.package import *


class AmrWind(CMakePackage, CudaPackage, ROCmPackage):
    """AMR-Wind is a massively parallel, block-structured adaptive-mesh,
    incompressible flow sover for wind turbine and wind farm simulations."""

    homepage = "https://github.com/Exawind/amr-wind"
    url = "https://github.com/Exawind/amr-wind/archive/refs/tags/v1.3.0.tar.gz"
    git = "https://github.com/Exawind/amr-wind.git"

    maintainers("jrood-nrel", "psakievich")

    tags = ["ecp", "ecp-apps"]

    license("BSD-3-Clause")

    version("main", branch="main", submodules=True)
    version(
        "3.4.2", tag="v3.4.2", commit="ed475a0533dfacf1fdff0b707518ccf99040d9f9", submodules=True
    )
    version(
        "3.4.1", tag="v3.4.1", commit="effe63ca9061e6d2bd5c5e84b690d29c0869f029", submodules=True
    )
    version(
        "3.4.0", tag="v3.4.0", commit="38d1b9fd0b70aab4a01fd507f039750c2508bd1c", submodules=True
    )
    version(
        "3.3.1", tag="v3.3.1", commit="30fc9a15a65670ebe3226b85e76b2155b4e4251d", submodules=True
    )
    version(
        "3.3.0", tag="v3.3.0", commit="cba28f0fb9d7c5c6d1aeb57e67469c962f9a12d4", submodules=True
    )
    version(
        "3.2.3", tag="v3.2.3", commit="a609630eb7e21f6054a40d34865b2e7dd2be4eab", submodules=True
    )
    version(
        "3.2.2", tag="v3.2.2", commit="e12ec7b5a973a7e9d57dffdbf9a2875c601bb0cf", submodules=True
    )
    version(
        "3.2.1", tag="v3.2.1", commit="2b309bdb578d549eba08cd8bdf852aa85fbb33f2", submodules=True
    )
    version(
        "3.2.0", tag="v3.2.0", commit="bb0e9dcc59c694812a03703199ade0a3984161d5", submodules=True
    )
    version(
        "3.1.7", tag="v3.1.7", commit="b9858be2c7ae85ad3c78e414699fad4acf2a7a22", submodules=True
    )
    version(
        "3.1.6", tag="v3.1.6", commit="ca437affc6fd00490d8b14e244e53bf641207224", submodules=True
    )
    version(
        "3.1.5", tag="v3.1.5", commit="554f8aa1ac36c2bae17565c64d5bc33333cee396", submodules=True
    )
    version(
        "3.1.4", tag="v3.1.4", commit="e10f5ebd3141b9990a65ebe9f1bdca8554b59472", submodules=True
    )
    version(
        "3.1.3", tag="v3.1.3", commit="af8231ace69119133c4c8a906e98946ec5aa79c8", submodules=True
    )
    version(
        "3.1.2", tag="v3.1.2", commit="5edcac4496e30e450c0f21e7fa74f8b590dc3860", submodules=True
    )
    version(
        "3.1.1", tag="v3.1.1", commit="8ae06194fa47bf473615988f97a7b423d467b023", submodules=True
    )
    version(
        "3.1.0", tag="v3.1.0", commit="3e23581b132532bf70b09c38217ff9c46204f047", submodules=True
    )
    version(
        "3.0.2", tag="v3.0.2", commit="f867288dffecc6404189afa965189c2558cf9922", submodules=True
    )
    version(
        "3.0.1", tag="v3.0.1", commit="65aa85db5cb3bbabc767d5dde4b106b7022a0f90", submodules=True
    )
    version(
        "3.0.0", tag="v3.0.0", commit="2fbd345cfa7cb7277c1cb6a1323247579e1bbc32", submodules=True
    )
    with default_args(deprecated=True):
        version(
            "2.6.0",
            tag="v2.6.0",
            commit="31ef1137b00b304b62b84edaa5b819c0bf0b7436",
            submodules=True,
        )
        version(
            "2.5.0",
            tag="v2.5.0",
            commit="f9f499b6926339f96b3ff260495b8782c045555c",
            submodules=True,
        )
        version(
            "2.4.3",
            tag="v2.4.3",
            commit="4be85f376d4939f8e5534b7985917e4cfccedfaf",
            submodules=True,
        )
        version(
            "2.4.2",
            tag="v2.4.2",
            commit="5ebb2abf2df9c87e6086d8f55a4d929ff0cdb37b",
            submodules=True,
        )
        version(
            "2.4.1",
            tag="v2.4.1",
            commit="40accd372f850e10fcbeee6ddecc4d15fd6364c6",
            submodules=True,
        )
        version(
            "2.4.0",
            tag="v2.4.0",
            commit="b8ab898b7e9e8e78455b61e303940b80d00d18ca",
            submodules=True,
        )
        version(
            "2.3.2",
            tag="v2.3.2",
            commit="61cbb21e8dfdeea47a0add772cd52abac33c4901",
            submodules=True,
        )
        version(
            "2.3.1",
            tag="v2.3.1",
            commit="cc51dadb34de9f333605a5bfb83b72c9310f676a",
            submodules=True,
        )
        version(
            "2.3.0",
            tag="v2.3.0",
            commit="6ba000b628aa3178545cdbbea508cc2cb2e5c76c",
            submodules=True,
        )
        version(
            "2.2.1",
            tag="v2.2.1",
            commit="e131a79f8e68be181390a2656f54268f90a9e78a",
            submodules=True,
        )
        version(
            "2.2.0",
            tag="v2.2.0",
            commit="bc787f21deca9239928182e27400133934c62658",
            submodules=True,
        )
        version(
            "2.1.0",
            tag="v2.1.0",
            commit="13e15b52f4a1651a3d72324a71ba1e18255663e7",
            submodules=True,
        )
        version(
            "2.0.0",
            tag="v2.0.0",
            commit="ea448365033fc6bc9ee0febeb369b377f4fd8240",
            submodules=True,
        )
        version(
            "1.4.0",
            tag="v1.4.0",
            commit="bdddf133e41a9b7b4c8ce28f1ea1bebec47678f5",
            submodules=True,
        )
        version(
            "1.3.1",
            tag="v1.3.1",
            commit="63692889143599de57232e64a9c7e4af8f0a2e1e",
            submodules=True,
        )
        version(
            "1.3.0",
            tag="v1.3.0",
            commit="f74d7b3801f0492e586d440fac729d9dec595a8b",
            submodules=True,
        )
        version(
            "1.2.1",
            tag="v1.2.1",
            commit="7291737434ca339ecc765355eab88ddd529ff68f",
            submodules=True,
        )
        version(
            "1.2.0",
            tag="v1.2.0",
            commit="db9add5c1c68583a9019cb7ba6776bd580b0ab3e",
            submodules=True,
        )
        version(
            "1.1.0",
            tag="v1.1.0",
            commit="30396bf70f0bd5ac65dd0f7b29757b0e02b22459",
            submodules=True,
        )
        version(
            "1.0.1",
            tag="v1.0.1",
            commit="aa9b7e8e63833e6ac1cc3f60fcba5140416cc139",
            submodules=True,
        )
        version(
            "1.0.0",
            tag="v1.0.0",
            commit="885f4137ce7b9e6c60f48aa5e4c1a54f1418ea9e",
            submodules=True,
        )
        version(
            "0.9.0",
            tag="v0.9.0",
            commit="cf66ebe31fd5f27b76a83451cd22f346e7a67160",
            submodules=True,
        )

    variant("hypre", default=False, description="Enable Hypre integration")
    variant("ascent", default=False, description="Enable Ascent integration")
    variant("masa", default=False, description="Enable MASA integration")
    variant("mpi", default=True, description="Enable MPI support")
    variant("netcdf", default=False, description="Enable NetCDF support")
    variant("openfast", default=False, description="Enable OpenFAST integration")
    variant("openmp", default=False, description="Enable OpenMP for CPU builds")
    variant("shared", default=True, description="Build shared libraries")
    variant("tests", default=True, description="Activate regression tests")
    variant("tiny_profile", default=False, description="Activate tiny profile")
    variant("hdf5", default=False, description="Enable HDF5 plots with ZFP compression")
    variant("umpire", default=False, description="Enable UMPIRE memory pooling")
    variant("sycl", default=False, description="Enable SYCL backend")
    variant("gpu-aware-mpi", default=False, description="Enable GPU aware MPI")
    variant("helics", default=False, description="Enable HELICS support for control interface")
    variant(
        "waves2amr", default=False, description="Enable Waves2AMR support for ocean wave input"
    )
    variant("fft", default=False, description="Enable FFT support for MAC projection")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build", when="+openfast")
    depends_on("mpi", when="+mpi")
    depends_on("hdf5~mpi", when="+hdf5~mpi")
    depends_on("hdf5+mpi", when="+hdf5+mpi")
    # New versions of HDF5 have CMake problems finding ZLIB::ZLIB target
    depends_on("hdf5@:1.14.4-3", when="+hdf5")
    depends_on("h5z-zfp", when="+hdf5")
    depends_on("zfp", when="+hdf5")
    depends_on("hypre~int64@2.29.0:", when="@0.9.0:+hypre")
    depends_on("hypre+mpi", when="+hypre+mpi")
    depends_on("hypre+umpire", when="+hypre+umpire")
    depends_on("hypre+sycl", when="+hypre+sycl")
    depends_on("hypre+gpu-aware-mpi", when="+hypre+gpu-aware-mpi")
    depends_on("masa", when="+masa")
    depends_on("ascent~mpi", when="+ascent~mpi")
    depends_on("ascent+mpi", when="+ascent+mpi")
    depends_on("netcdf-c", when="+netcdf")
    depends_on("py-netcdf4", when="+netcdf")
    depends_on("py-numpy@2:", when="+netcdf")
    depends_on("py-matplotlib", when="+masa")
    depends_on("py-pandas", when="+masa")
    depends_on("openfast+cxx", when="+openfast")
    depends_on("openfast+netcdf", when="+openfast+netcdf")
    depends_on("openfast@2.6.0:3.4.1", when="@0.9.0:1 +openfast")
    depends_on("openfast@3.5:", when="@2: +openfast")
    depends_on("helics@:3.3.2", when="+helics")
    depends_on("helics@:3.3.2+mpi", when="+helics+mpi")
    depends_on("fftw", when="@2.1: +waves2amr")
    depends_on("fftw", when="@3.3.1: +fft")

    depends_on("rocrand", when="+rocm")
    depends_on("rocprim", when="+rocm")

    for arch in CudaPackage.cuda_arch_values:
        depends_on("hypre+cuda cuda_arch=%s" % arch, when="+cuda+hypre cuda_arch=%s" % arch)
    for arch in ROCmPackage.amdgpu_targets:
        depends_on(
            "hypre+rocm amdgpu_target=%s" % arch, when="+rocm+hypre amdgpu_target=%s" % arch
        )
    for arch in CudaPackage.cuda_arch_values:
        depends_on("ascent+cuda cuda_arch=%s" % arch, when="+ascent+cuda cuda_arch=%s" % arch)

    conflicts("+openmp", when="+cuda")
    conflicts("+shared", when="+cuda")
    conflicts("@:2.0", when="+waves2amr")
    conflicts(
        "openfast@4.0.0:4.0.1", msg="OpenFAST 4.0.0:4.0.1 contains a bug. Use OpenFAST >= 4.0.2."
    )

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        # Avoid compile errors with Intel interprocedural optimization
        if self.spec.satisfies("%intel"):
            env.append_flags("CXXFLAGS", "-no-ipo")
        if self.spec.satisfies("+cuda"):
            env.set("CUDAHOSTCXX", spack_cxx)

    def cmake_args(self):
        define = self.define
        spec = self.spec

        vs = [
            "mpi",
            "cuda",
            "openmp",
            "netcdf",
            "hypre",
            "masa",
            "ascent",
            "openfast",
            "rocm",
            "tests",
            "tiny_profile",
            "fft",
            "helics",
            "umpire",
            "sycl",
        ]
        args = [self.define_from_variant("AMR_WIND_ENABLE_%s" % v.upper(), v) for v in vs]

        args += [self.define_from_variant("BUILD_SHARED_LIBS", "shared")]

        if spec.satisfies("+mpi"):
            args.append(define("MPI_HOME", spec["mpi"].prefix))
            args.append(define("MPI_CXX_COMPILER", spec["mpi"].mpicxx))
            args.append(define("MPI_C_COMPILER", spec["mpi"].mpicc))

        if spec.satisfies("+hdf5"):
            args.append(define("AMR_WIND_ENABLE_HDF5", True))
            args.append(define("AMR_WIND_ENABLE_HDF5_ZFP", True))
            # Help AMReX understand if HDF5 is parallel or not.
            # Building HDF5 with CMake as Spack does, causes this inspection to break.
            args.append(define("HDF5_IS_PARALLEL", spec.satisfies("+mpi")))

        if spec.satisfies("+cuda"):
            args.append(define("CMAKE_CUDA_ARCHITECTURES", spec.variants["cuda_arch"].value))

        if spec.satisfies("+rocm"):
            args.append(define("CMAKE_CXX_COMPILER", spec["hip"].hipcc))
            targets = spec.variants["amdgpu_target"].value
            args.append("-DAMReX_AMD_ARCH=" + ";".join(str(x) for x in targets))

        if spec.satisfies("+umpire"):
            args.append(define("UMPIRE_DIR", spec["umpire"].prefix))

        if spec.satisfies("+helics"):
            args.append(define("HELICS_DIR", spec["helics"].prefix))

        if spec.satisfies("+waves2amr"):
            args.append(self.define_from_variant("AMR_WIND_ENABLE_W2A", "waves2amr"))
            args.append(define("FFTW_DIR", spec["fftw"].prefix))

        if spec.satisfies("+fft"):
            args.append(define("FFTW_DIR", spec["fftw"].prefix))

        if spec.satisfies("+sycl"):
            requires(
                "%dpcpp",
                "%oneapi",
                policy="one_of",
                msg=(
                    "AMReX's SYCL GPU Backend requires DPC++ (dpcpp) "
                    "or the oneAPI CXX (icpx) compiler."
                ),
            )

        if spec.satisfies("+openfast"):
            args.append(define("AMR_WIND_OPENFAST_VERSION", spec["openfast"].version))

        return args
