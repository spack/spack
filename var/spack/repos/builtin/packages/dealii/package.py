# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Dealii(CMakePackage, CudaPackage):
    """C++ software library providing well-documented tools to build finite
    element codes for a broad variety of PDEs."""

    homepage = "https://www.dealii.org"
    url = "https://github.com/dealii/dealii/releases/download/v8.4.1/dealii-8.4.1.tar.gz"
    git = "https://github.com/dealii/dealii.git"

    maintainers("jppelteret", "luca-heltai")

    # Don't add RPATHs to this package for the full build DAG.
    # only add for immediate deps.
    transitive_rpaths = False

    # FIXME nvcc_wrapper (used for +clang) doesn't handle response files
    # correctly when ninja is used. Those are used automatically if paths get too long.
    generator("make")

    version("master", branch="master")
    version("9.5.1", sha256="a818b535e6488d3aef7853311657c7b4fadc29a9abe91b7b202b131aad630f5e")
    version("9.5.0", sha256="a81f41565f0d3a22d491ee687957dd48053225da72e8d6d628d210358f4a0464")
    version("9.4.2", sha256="45a76cb400bfcff25cc2d9093d9a5c91545c8367985e6798811c5e9d2a6a6fd4")
    version("9.4.1", sha256="bfe5e4bf069159f93feb0f78529498bfee3da35baf5a9c6852aa59d7ea7c7a48")
    version("9.4.0", sha256="238677006cd9173658e5b69cdd1861f800556982db6005a3cc5eb8329cc1e36c")
    version("9.3.3", sha256="5dfb59174b341589e92b434398a1b7cc11ad053ce2315cf673f5efc5ba271a29")
    version("9.3.2", sha256="5341d76bfd75d3402fc6907a875513efb5fe8a8b99af688d94443c492d5713e8")
    version("9.3.1", sha256="a62f4676ab2dc029892251d141427fb75cbb83cddd606019f615d0dde9c61ab8")
    version("9.3.0", sha256="aef8c7a87510ce827dfae3bdd4ed7bff82004dc09f96fa7a65b2554f2839b931")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # Configuration variants
    variant(
        "build_type",
        default="DebugRelease",
        description="The build type to build",
        values=("Debug", "Release", "DebugRelease"),
    )
    variant(
        "cxxstd",
        default="14",
        when="@9.3:9.5",
        multi=False,
        description="Compile using the specified C++ standard",
        values=("default", "14", "17"),
    )
    variant(
        "cxxstd",
        default="17",
        when="@9.6:",
        multi=False,
        description="Compile using the specified C++ standard",
        values=("default", "17"),
    )
    variant("doc", default=False, description="Compile with documentation")
    variant("examples", default=True, description="Compile and install tutorial programs")
    variant("int64", default=False, description="Compile with 64 bit indices support")
    variant("mpi", default=True, description="Compile with MPI")
    variant("optflags", default=False, description="Compile using additional optimization flags")
    variant("platform-introspection", default=True, description="Enable platform introspection")
    variant("python", default=False, description="Compile with Python bindings")

    # Package variants
    variant("assimp", default=True, description="Compile with Assimp")
    variant("arborx", default=True, description="Compile with Arborx support")
    variant("arpack", default=True, description="Compile with Arpack and PArpack (only with MPI)")
    variant("adol-c", default=True, description="Compile with ADOL-C")
    variant("cgal", default=True, when="@9.4:~cuda", description="Compile with CGAL")
    variant("ginkgo", default=True, description="Compile with Ginkgo")
    variant("gmsh", default=True, description="Compile with GMSH")
    variant("gsl", default=True, description="Compile with GSL")
    variant("hdf5", default=True, description="Compile with HDF5 (only with MPI)")
    variant("kokkos", default=True, when="@9.5:", description="Compile with Kokkos")
    variant("metis", default=True, description="Compile with Metis")
    variant("muparser", default=True, description="Compile with muParser")
    variant("netcdf", default=False, description="Compile with Netcdf (only with MPI)")
    variant("oce", default=True, description="Compile with OCE")
    variant("p4est", default=True, description="Compile with P4est (only with MPI)")
    variant("petsc", default=True, description="Compile with Petsc (only with MPI)")
    variant("scalapack", default=True, description="Compile with ScaLAPACK (only with MPI)")
    variant("sundials", default=True, description="Compile with Sundials")
    variant("slepc", default=True, description="Compile with Slepc (only with Petsc and MPI)")
    variant("symengine", default=True, description="Compile with SymEngine")
    variant("simplex", default=True, description="Compile with Simplex support")
    variant(
        "taskflow",
        default=False,
        when="@9.6:",
        description="Compile with multi-threading via Taskflow",
    )
    variant("threads", default=True, description="Compile with multi-threading via TBB")
    variant("trilinos", default=True, description="Compile with Trilinos (only with MPI)")
    variant("vtk", default=True, when="@9.6:", description="Compile with VTK")

    # Required dependencies: Light version
    depends_on("blas")
    # Boost 1.58 is blacklisted, require at least 1.59, see
    # https://github.com/dealii/dealii/issues/1591
    # There are issues with 1.65.1 and 1.65.0:
    # https://github.com/dealii/dealii/issues/5262
    # we take the patch from https://github.com/boostorg/serialization/pull/79
    # more precisely its variation https://github.com/dealii/dealii/pull/5572#issuecomment-349742019
    # 1.68.0 has issues with serialization https://github.com/dealii/dealii/issues/7074
    # adopt https://github.com/boostorg/serialization/pull/105 as a fix
    #
    # dealii does not build with Boost 1.80.0
    # (https://github.com/spack/spack/pull/32879#issuecomment-1265933265)
    depends_on(
        "boost@1.59.0:1.63,1.65.1,1.67.0:1.79+thread+system+serialization+iostreams",
        patches=[
            patch("boost_1.65.1_singleton.patch", level=1, when="@1.65.1"),
            patch("boost_1.68.0.patch", level=1, when="@1.68.0"),
        ],
        when="~python",
    )
    depends_on(
        "boost@1.59.0:1.63,1.65.1,1.67.0:1.79+thread+system+serialization+iostreams+python",
        patches=[
            patch("boost_1.65.1_singleton.patch", level=1, when="@1.65.1"),
            patch("boost_1.68.0.patch", level=1, when="@1.68.0"),
        ],
        when="+python",
    )
    # The std::auto_ptr is removed in the C++ 17 standard.
    # See https://github.com/dealii/dealii/issues/4662
    # and related topics discussed for other software libraries.
    depends_on("boost cxxstd=14", when="cxxstd=14")
    depends_on("boost cxxstd=17", when="cxxstd=17")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("lapack")
    depends_on("suite-sparse")
    depends_on("zlib-api")

    # Optional dependencies: Configuration
    depends_on("cuda@8:", when="+cuda")
    depends_on("cmake@3.9:", when="+cuda", type="build")
    depends_on("cmake@3.1.0:", when="@9.3:9.4", type="build")
    depends_on("cmake@3.3.0:", when="@9.4:9.5", type="build")
    depends_on("cmake@3.13.4:", when="@9.5:", type="build")
    depends_on("mpi", when="+mpi")
    depends_on("python", when="@8.5.0:+python")

    # Optional dependencies: Packages
    depends_on("adol-c@2.6.4:", when="@9.0:+adol-c")
    depends_on("arborx", when="@9.3:+arborx")
    depends_on("arborx+trilinos", when="@9.3:+arborx+trilinos")
    depends_on("arpack-ng+mpi", when="+arpack+mpi")
    depends_on("assimp", when="@9.0:+assimp")
    depends_on("cgal", when="@9.4:+cgal")
    depends_on("cgal@5:", when="@9.5:+cgal")
    depends_on("doxygen+graphviz", when="+doc")
    depends_on("graphviz", when="+doc")
    depends_on("ginkgo", when="@9.1:+ginkgo")
    depends_on("ginkgo@1.4.0:", when="@9.4:+ginkgo")
    depends_on("gmsh+tetgen+netgen+oce", when="@9.0:+gmsh", type=("build", "run"))
    depends_on("gsl", when="@8.5.0:+gsl")
    # TODO: next line fixes concretization with petsc
    depends_on("hdf5+mpi+hl+fortran", when="+hdf5+mpi+petsc")
    depends_on("hdf5+mpi+hl", when="+hdf5+mpi~petsc")
    depends_on("kokkos@3.7:", when="@9.5:+kokkos~trilinos")
    depends_on("kokkos@3.7:+cuda+cuda_lambda+wrapper", when="@9.5:+kokkos~trilinos+cuda")
    # TODO: concretizer bug. The two lines mimic what comes from PETSc
    # but we should not need it
    depends_on("metis@5:+int64", when="+metis+int64")
    depends_on("metis@5:~int64", when="+metis~int64")
    depends_on("muparser", when="+muparser")
    depends_on("netcdf-c+mpi", when="+netcdf+mpi")
    depends_on("netcdf-cxx", when="+netcdf+mpi")
    depends_on("oce", when="+oce")
    depends_on("p4est", when="+p4est+mpi")
    depends_on("petsc+mpi~int64", when="+petsc+mpi~int64")
    depends_on("petsc+mpi+int64", when="+petsc+mpi+int64")
    depends_on("scalapack", when="@9.0:+scalapack")
    depends_on("slepc", when="+slepc+petsc+mpi")
    depends_on("slepc~arpack", when="+slepc+petsc+mpi+int64")
    depends_on("sundials@:3~pthread", when="@9.0:9.2+sundials")
    depends_on("sundials@5:5.8", when="@9.3:9.3.3+sundials")
    depends_on("sundials@5:6.7", when="@9.3.4:+sundials")
    depends_on("taskflow@3.4:", when="@9.6:+taskflow")
    depends_on("trilinos gotype=int", when="+trilinos@12.18.1:")
    # TODO: next line fixes concretization with trilinos and adol-c
    depends_on("trilinos~exodus", when="@9.0:+adol-c+trilinos")
    # Both Trilinos and SymEngine bundle the Teuchos RCP library.
    # This leads to conflicts between macros defined in the included
    # headers when they are not compiled in the same mode.
    # See https://github.com/symengine/symengine/issues/1516
    # TODO: uncomment when the following is fixed
    # https://github.com/spack/spack/issues/11160
    # depends_on(
    #     "symengine@0.4: build_type=Release",
    #     when="@9.1:+symengine+trilinos^trilinos~debug"
    # )
    # depends_on(
    #     "symengine@0.4: build_type=Debug",
    #     when="@9.1:+symengine+trilinos^trilinos+debug"
    # )
    depends_on("symengine@0.4:", when="@9.1:+symengine")
    depends_on("symengine@0.6:", when="@9.2:+symengine")
    depends_on("tbb", when="+threads")
    # do not require +rol to make concretization of xsdk possible
    depends_on("trilinos+amesos+aztec+epetra+ifpack+ml+muelu+sacado", when="+trilinos")
    depends_on("trilinos~hypre", when="+trilinos+int64")
    for _arch in CudaPackage.cuda_arch_values:
        arch_str = f"+cuda cuda_arch={_arch}"
        trilinos_spec = f"trilinos +wrapper {arch_str}"
        depends_on(trilinos_spec, when=f"@9.5:+trilinos {arch_str}")
    depends_on("vtk", when="@9.6:+vtk")

    # Fix issues due to override of CMake FIND_PACKAGE macro
    # https://github.com/dealii/dealii/pull/14158/files
    patch(
        "https://github.com/dealii/dealii/commit/06bb9dc07efb6fea9912ee0d66264af548c552c8.patch?full_index=1",
        sha256="8a1f7b9a155c8c496ce08b2abb1ba5d329b3b29169f36c11678aa4e3cebf97a2",
        when="@9.4 ^hdf5",
    )
    patch(
        "https://github.com/dealii/dealii/commit/40076ac1a013cd7d221f9dda913b4d0e6452c21e.patch?full_index=1",
        sha256="7869dfab1116b6e862279bb6642c2c8fe49d87c42cfc6f031e03330f9f26a6c3",
        when="@9.4 ^python",
    )

    # Fix issues with the FIND_GINKGO module for the newer Ginkgo versions
    # https://github.com/dealii/dealii/pull/14413
    patch(
        "https://github.com/dealii/dealii/commit/df6c5de8d6785fce701c10575982858f3aeb4cbd.patch?full_index=1",
        sha256="c9884ebb0fe379c539012a225d8bcdcfe288edec8dc9d319fbfd64d8fbafba8e",
        when="@:9.4 +ginkgo ^ginkgo@1.5.0:",
    )

    # deal.II's own CUDA backend does not support CUDA version 12.0 or newer.
    conflicts("+cuda ^cuda@12:")

    # Check for sufficiently modern versions
    conflicts("cxxstd=11", when="@9.3:")

    conflicts(
        "cxxstd=14",
        when="@9.4:+cgal",
        msg="CGAL requires the C++ standard to be set to 17 or later.",
    )

    conflicts(
        "cxxstd=default",
        when="@9.4:+cgal",
        msg="CGAL requires the C++ standard to be set explicitly to 17 or later.",
    )

    conflicts(
        "cxxstd=14",
        when="@9.6:",
        msg="deal.II 9.6 onwards requires the C++ standard to be set to 17 or later.",
    )

    # Interfaces added after 9.5.0:
    for _package in ["vtk", "taskflow"]:
        conflicts(
            "+{0}".format(_package),
            when="@:9.5",
            msg="The interface to {0} is supported from version 9.6.0 "
            "onwards. Please explicitly disable this variant "
            "via ~{0}".format(_package),
        )

    # MPI requirements:
    for _package in [
        "arpack",
        "hdf5",
        "netcdf",
        "p4est",
        "petsc",
        "scalapack",
        "slepc",
        "trilinos",
    ]:
        conflicts(
            "+{0}".format(_package),
            when="~mpi",
            msg="To enable {0} it is necessary to build deal.II with "
            "MPI support enabled.".format(_package),
        )

    # Optional dependencies:
    conflicts("+adol-c", when="+netcdf", msg="Symbol clash between the ADOL-C library and Netcdf.")
    conflicts(
        "+adol-c",
        when="^trilinos+chaco",
        msg="Symbol clash between the ADOL-C library and " "Trilinos SEACAS Chaco.",
    )
    conflicts(
        "+adol-c",
        when="^trilinos+exodus",
        msg="Symbol clash between the ADOL-C library and " "Trilinos Netcdf.",
    )

    conflicts(
        "+slepc",
        when="~petsc",
        msg="It is not possible to enable slepc interfaces " "without petsc.",
    )

    def cmake_args(self):
        spec = self.spec
        options = []
        # Release flags
        cxx_flags_release = []
        # Debug and release flags
        cxx_flags = []

        # Set directory structure:
        options.extend(
            [
                self.define("DEAL_II_EXAMPLES_RELDIR", "share/deal.II/examples"),
                self.define("DEAL_II_DOCREADME_RELDIR", "share/deal.II/"),
                self.define("DEAL_II_DOCHTML_RELDIR", "share/deal.II/doc"),
            ]
        )

        # Required dependencies
        lapack_blas_libs = spec["lapack"].libs + spec["blas"].libs
        lapack_blas_headers = spec["lapack"].headers + spec["blas"].headers
        options.extend(
            [
                self.define("BOOST_DIR", spec["boost"].prefix),
                # CMake's FindBlas/Lapack may pickup system's blas/lapack instead
                # of Spack's. Be more specific to avoid this.
                # Note that both lapack and blas are provided in -DLAPACK_XYZ.
                self.define("LAPACK_FOUND", True),
                self.define("LAPACK_INCLUDE_DIRS", ";".join(lapack_blas_headers.directories)),
                self.define("LAPACK_LIBRARIES", lapack_blas_libs.joined(";")),
                self.define("UMFPACK_DIR", spec["suite-sparse"].prefix),
                self.define("ZLIB_DIR", spec["zlib-api"].prefix),
                self.define("DEAL_II_ALLOW_BUNDLED", False),
            ]
        )

        # Doxygen documentation
        options.append(self.define_from_variant("DEAL_II_COMPONENT_DOCUMENTATION", "doc"))

        # Examples / tutorial programs
        options.append(self.define_from_variant("DEAL_II_COMPONENT_EXAMPLES", "examples"))
        options.append(self.define_from_variant("DEAL_II_COMPILE_EXAMPLES", "examples"))

        # Enforce the specified C++ standard
        if spec.variants["cxxstd"].value != "default":
            cxxstd = spec.variants["cxxstd"].value
            cxx_flags.extend(["-std=c++{0}".format(cxxstd)])

        # Performance
        # Set recommended flags for maximum (matrix-free) performance, see
        # https://groups.google.com/forum/?fromgroups#!topic/dealii/3Yjy8CBIrgU
        if spec.satisfies("%gcc"):
            cxx_flags_release.extend(["-O3"])
        elif spec.satisfies("%intel"):
            cxx_flags_release.extend(["-O3"])
        elif spec.satisfies("%clang") or spec.satisfies("%apple-clang"):
            cxx_flags_release.extend(["-O3", "-ffp-contract=fast"])

        # 64 bit indices
        options.append(self.define_from_variant("DEAL_II_WITH_64BIT_INDICES", "int64"))

        if (
            spec.satisfies("^openblas+ilp64")
            or spec.satisfies("^intel-mkl+ilp64")
            or spec.satisfies("^intel-parallel-studio+mkl+ilp64")
        ):
            options.append(self.define("LAPACK_WITH_64BIT_BLAS_INDICES", True))

        # CUDA
        options.append(self.define_from_variant("DEAL_II_WITH_CUDA", "cuda"))
        if "+cuda" in spec:
            if not spec.satisfies("^cuda@9:"):
                options.append("-DDEAL_II_WITH_CXX14=OFF")
            cuda_arch = spec.variants["cuda_arch"].value
            if cuda_arch != "none":
                if len(cuda_arch) > 1:
                    raise InstallError("deal.II only supports compilation for a single GPU!")
                flags = "-arch=sm_{0}".format(cuda_arch[0])
                # TODO: there are some compiler errors in dealii
                # with: flags = ' '.join(self.cuda_flags(cuda_arch))
                # Stick with -arch=sm_xy for now.
                options.append(self.define("DEAL_II_CUDA_FLAGS", flags))

        # MPI
        options.append(self.define_from_variant("DEAL_II_WITH_MPI", "mpi"))
        if "+mpi" in spec:
            options.extend(
                [
                    self.define("MPI_C_COMPILER", spec["mpi"].mpicc),
                    self.define("MPI_CXX_COMPILER", spec["mpi"].mpicxx),
                    self.define("MPI_Fortran_COMPILER", spec["mpi"].mpifc),
                ]
            )
            # FIXME: Fix issues with undefined references in MPI. e.g,
            # libmpi.so: undefined reference to `opal_memchecker_base_isaddressable'
            if "^openmpi" in spec:
                options.extend([self.define("MPI_CXX_LINK_FLAGS", "-lopen-pal")])
            if "+cuda" in spec:
                options.extend(
                    [
                        self.define(
                            "DEAL_II_MPI_WITH_CUDA_SUPPORT", spec["mpi"].satisfies("+cuda")
                        ),
                        self.define("CUDA_HOST_COMPILER", spec["mpi"].mpicxx),
                    ]
                )
            # Make sure we use the same compiler that Trilinos uses
            if "+trilinos" in spec:
                options.extend([self.define("CMAKE_CXX_COMPILER", spec["trilinos"].kokkos_cxx)])

        # Python bindings
        options.append(self.define_from_variant("DEAL_II_COMPONENT_PYTHON_BINDINGS", "python"))

        # Simplex support (no longer experimental)
        options.append(self.define_from_variant("DEAL_II_WITH_SIMPLEX_SUPPORT", "simplex"))

        # Threading
        options.append(self.define_from_variant("DEAL_II_WITH_TBB", "threads"))
        if "+threads" in spec:
            if spec.satisfies("^intel-parallel-studio+tbb"):
                # deal.II/cmake will have hard time picking up TBB from Intel.
                tbb_ver = ".".join(("%s" % spec["tbb"].version).split(".")[1:])
                options.extend(
                    [
                        self.define("TBB_FOUND", True),
                        self.define("TBB_VERSION", tbb_ver),
                        self.define("TBB_INCLUDE_DIRS", ";".join(spec["tbb"].headers.directories)),
                        self.define("TBB_LIBRARIES", spec["tbb"].libs.joined(";")),
                    ]
                )
            else:
                options.append(self.define("TBB_DIR", spec["tbb"].prefix))

        # Optional dependencies for which library names are the same as CMake
        # variables:
        for library in (
            "arborx",
            "assimp",
            "cgal",
            "ginkgo",
            "gmsh",
            "gsl",
            "hdf5",
            "metis",
            "muparser",
            "nanoflann",
            "p4est",
            "petsc",
            "slepc",
            "sundials",
            "symengine",
            "taskflow",
            "trilinos",
            "vtk",
        ):
            options.append(
                self.define_from_variant("DEAL_II_WITH_{0}".format(library.upper()), library)
            )
            if ("+" + library) in spec:
                options.append(
                    self.define("{0}_DIR".format(library.upper()), spec[library].prefix)
                )

        # Optional dependencies that do not fit the above pattern:
        # ADOL-C
        options.append(self.define_from_variant("DEAL_II_WITH_ADOLC", "adol-c"))
        if "+adol-c" in spec:
            options.append(self.define("ADOLC_DIR", spec["adol-c"].prefix))

        # ARPACK
        options.append(self.define_from_variant("DEAL_II_WITH_ARPACK", "arpack"))
        if "+arpack" in spec and "+mpi" in spec:
            options.extend(
                [
                    self.define("ARPACK_DIR", spec["arpack-ng"].prefix),
                    self.define("DEAL_II_ARPACK_WITH_PARPACK", True),
                ]
            )

        # NetCDF
        # since Netcdf is spread among two, need to do it by hand:
        if "+netcdf" in spec and "+mpi" in spec:
            netcdf_libs = spec["netcdf-cxx"].libs + spec["netcdf-c"].libs
            options.extend(
                [
                    self.define("NETCDF_FOUND", True),
                    self.define(
                        "NETCDF_INCLUDE_DIRS",
                        "{0};{1}".format(
                            spec["netcdf-cxx"].prefix.include, spec["netcdf-c"].prefix.include
                        ),
                    ),
                    self.define("NETCDF_LIBRARIES", netcdf_libs.joined(";")),
                ]
            )
        else:
            options.append(self.define("DEAL_II_WITH_NETCDF", False))

        # ScaLAPACK
        options.append(self.define_from_variant("DEAL_II_WITH_SCALAPACK", "scalapack"))
        if "+scalapack" in spec:
            scalapack_libs = spec["scalapack"].libs
            options.extend(
                [
                    self.define("SCALAPACK_FOUND", True),
                    self.define("SCALAPACK_INCLUDE_DIRS", spec["scalapack"].prefix.include),
                    self.define("SCALAPACK_LIBRARIES", scalapack_libs.joined(";")),
                    # If SCALAPACK_LIBRARY is not set, deal.II still searches
                    # for SCALAPACK despite the above settings:
                    self.define("SCALAPACK_LIBRARY", scalapack_libs.joined(";")),
                ]
            )

        # Open Cascade
        options.append(self.define_from_variant("DEAL_II_WITH_OPENCASCADE", "oce"))
        if "+oce" in spec:
            options.append(self.define("OPENCASCADE_DIR", spec["oce"].prefix))

        # As a final step, collect CXX flags that may have been
        # added anywhere above:
        if len(cxx_flags_release) > 0 and "+optflags" in spec:
            options.extend([self.define("CMAKE_CXX_FLAGS_RELEASE", " ".join(cxx_flags_release))])
        if len(cxx_flags) > 0:
            options.extend([self.define("CMAKE_CXX_FLAGS", " ".join(cxx_flags))])

        # Add flags for machine vectorization, used when tutorials
        # and user code is built.
        # See https://github.com/dealii/dealii/issues/9164
        options.append(self.define("DEAL_II_CXX_FLAGS", os.environ["SPACK_TARGET_ARGS"]))

        # platform introspection - needs to be disabled in some environments
        if "+platform-introspection" in spec:
            options.append(self.define("DEAL_II_ALLOW_PLATFORM_INTROSPECTION", True))
        else:
            options.append(self.define("DEAL_II_ALLOW_PLATFORM_INTROSPECTION", False))

        return options

    def setup_run_environment(self, env):
        env.set("DEAL_II_DIR", self.prefix)

    def setup_build_environment(self, env):
        spec = self.spec
        if "+cuda" in spec and "+mpi" in spec:
            env.set("CUDAHOSTCXX", spec["mpi"].mpicxx)
