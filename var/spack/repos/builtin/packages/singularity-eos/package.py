# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class SingularityEos(CMakePackage, CudaPackage):
    """Singularity-EOS: A collection of closure models and tools useful for
    multiphysics codes."""

    homepage = "https://lanl.github.io/singularity-eos/main/index.html"
    git = "https://github.com/lanl/singularity-eos.git"
    url = "https://github.com/lanl/singularity-eos/archive/refs/tags/release-1.6.1.tar.gz"

    maintainers("rbberger")

    version("main", branch="main")
    version("1.7.0", sha256="ce0825db2e9d079503e98cecf1c565352be696109042b3a0941762b35f36dc49")
    version("1.6.2", sha256="9c85fca679139a40cc9c72fcaeeca78a407cc1ca184734785236042de364b942")
    version("1.6.1", sha256="c6d92dfecf9689ffe2df615791c039f7e527e9f47799a862e26fa4e3420fe5d7")

    # build with kokkos, kokkos-kernels for offloading support
    variant("kokkos", default=False, description="Enable kokkos")
    variant(
        "kokkos-kernels", default=False, description="Enable kokkos-kernals for linear algebra"
    )

    variant("openmp", default=False, description="Enable openmp")

    # for compatibility with downstream projects
    variant("mpi", default=False, description="Build with MPI support")

    # build converters for sesame, stellarcollapse eos's
    variant(
        "build_extra",
        description="Build converters",
        values=any_combination_of("sesame", "stellarcollapse").with_default("none"),
    )

    # build the Fortran interface
    variant("fortran", default=True, description="Enable building fortran interface")

    # build the Python bindings
    variant("python", default=False, description="Enable building Python bindings")

    variant("eospac", default=True, description="Pull in EOSPAC")

    # building/testing/docs
    depends_on("cmake@3.14:", type="build")
    depends_on("catch2@2.13.7", type="test")
    depends_on("python@3:", when="+python")
    depends_on("py-pybind11@2.9.1:", when="+python")

    # linear algebra when not using GPUs
    depends_on("eigen@3.3.8", when="~cuda")

    depends_on("eospac", when="+eospac")
    depends_on("spiner")
    depends_on("spiner +kokkos", when="+kokkos")

    depends_on("mpark-variant")
    depends_on(
        "mpark-variant",
        patches=patch(
            "https://raw.githubusercontent.com/lanl/singularity-eos/main/utils/cuda_compatibility.patch",
            sha256="7b3eaa52b5ab23dc45fbfb456528e36742e04b838a5df859eca96c4e8274bb38",
        ),
        when="+cuda",
    )

    # set up kokkos offloading dependencies
    for _flag in ("~cuda", "+cuda", "~openmp", "+openmp"):
        depends_on("kokkos@3.2: ~shared" + _flag, when="+kokkos" + _flag)
        depends_on("kokkos-kernels@3.2:" + _flag, when="+kokkos-kernels" + _flag)
        depends_on("spiner" + _flag, when="+kokkos" + _flag)

    # specfic specs when using GPU/cuda offloading
    depends_on("kokkos +wrapper+cuda_lambda+cuda_relocatable_device_code", when="+cuda+kokkos")

    # fix for older spacks
    if spack.version.Version(spack.spack_version) >= spack.version.Version("0.17"):
        depends_on("kokkos-kernels ~shared", when="+kokkos-kernels")

    for _flag in list(CudaPackage.cuda_arch_values):
        depends_on("kokkos cuda_arch=" + _flag, when="+cuda+kokkos cuda_arch=" + _flag)
        depends_on("kokkos-kernels cuda_arch=" + _flag, when="+cuda+kokkos cuda_arch=" + _flag)
        depends_on("spiner cuda_arch=" + _flag, when="+cuda+kokkos cuda_arch=" + _flag)

    conflicts("cuda_arch=none", when="+cuda", msg="CUDA architecture is required")

    # NOTE: we can do depends_on("libfoo cppflags='-fPIC -O2'") for compiler options

    # these are mirrored in the cmake configuration
    conflicts("+cuda", when="~kokkos")
    conflicts("+openmp", when="~kokkos")
    conflicts("+kokkos-kernels", when="~kokkos")

    # NOTE: these are set so that dependencies in downstream projects share
    # common MPI dependence
    for _flag in ("~mpi", "+mpi"):
        depends_on("hdf5~cxx+hl" + _flag, when=_flag)
        depends_on("py-h5py" + _flag, when="@:1.6.2 " + _flag)
        depends_on("kokkos-nvcc-wrapper" + _flag, when="+cuda+kokkos" + _flag)

    def flag_handler(self, name, flags):
        if name == "fflags":
            if self.spec.satisfies("%cce+fortran"):
                # The Cray fortran compiler generates module files with
                # uppercase names by default, which is not handled by the
                # CMake scripts. The following flag forces the compiler to
                # produce module files with lowercase names.
                flags.append("-ef")
        return (flags, None, None)

    def cmake_args(self):
        args = [
            self.define("SINGULARITY_PATCH_MPARK_VARIANT", False),
            self.define_from_variant("SINGULARITY_USE_CUDA", "cuda"),
            self.define_from_variant("SINGULARITY_USE_KOKKOS", "kokkos"),
            self.define_from_variant("SINGULARITY_USE_KOKKOSKERNELS", "kokkos-kernels"),
            self.define_from_variant("SINGULARITY_USE_FORTRAN", "fortran"),
            self.define_from_variant("SINGULARITY_BUILD_CLOSURE", "fortran"),
            self.define_from_variant("SINGULARITY_BUILD_PYTHON", "python"),
            self.define("SINGULARITY_BUILD_TESTS", self.run_tests),
            self.define(
                "SINGULARITY_BUILD_SESAME2SPINER",
                "sesame" in self.spec.variants["build_extra"].value,
            ),
            self.define(
                "SINGULARITY_TEST_SESAME",
                ("sesame" in self.spec.variants["build_extra"].value and self.run_tests),
            ),
            self.define(
                "SINGULARITY_BUILD_STELLARCOLLAPSE2SPINER",
                "stellarcollapse" in self.spec.variants["build_extra"].value,
            ),
            self.define(
                "SINGULARITY_TEST_STELLARCOLLAPSE2SPINER",
                ("stellarcollapse" in self.spec.variants["build_extra"].value and self.run_tests),
            ),
            self.define("SINGULARITY_TEST_PYTHON", ("+python" in self.spec and self.run_tests)),
            self.define("SINGULARITY_USE_HDF5", "^hdf5" in self.spec),
            self.define("SINGULARITY_USE_EOSPAC", "^eospac" in self.spec),
        ]

        if "+kokkos+cuda" in self.spec:
            args.append(self.define("CMAKE_CXX_COMPILER", self.spec["kokkos"].kokkos_cxx))

        return args

    # specify the name of the auto-generated cmake cache config
    @property
    def cmake_config_fname(self):
        return "singularity-eos_spackconfig.cmake"

    # generate the pre-configured cmake cache file that reflects the spec options
    # NOTE: this file isn't replaced if the same spec is already installed -
    # you may need to uninstall the old spec first
    @run_after("cmake")
    def generate_cmake_configuration(self):
        config_fname = self.cmake_config_fname
        cmake_config = self.cmake_args()

        with working_dir("cmake-gen", create=True):
            with open(config_fname, "w") as cmc:
                for arg in cmake_config:
                    kt, v = arg.replace("-D", "").split("=")
                    k, t = kt.split(":")
                    cmc.write('set({} "{}" CACHE {} "" FORCE)\n'.format(k, v, t))
            install(config_fname, join_path(prefix, config_fname))

    # run when loaded
    # NOTE: to use:
    #   cmake -C $SINGULARITY_SPACK_CMAKE_CONFIG ...
    def setup_run_environment(self, env):
        env.set(
            "SINGULARITY_SPACK_CMAKE_CONFIG", os.path.join(self.prefix, self.cmake_config_fname)
        )
        if os.path.isdir(self.prefix.lib64):
            lib_dir = self.prefix.lib64
        else:
            lib_dir = self.prefix.lib

        if "+python" in self.spec:
            python_version = self.spec["python"].version.up_to(2)
            python_inst_dir = join_path(
                lib_dir, "python{0}".format(python_version), "site-packages"
            )
            env.prepend_path("PYTHONPATH", python_inst_dir)
