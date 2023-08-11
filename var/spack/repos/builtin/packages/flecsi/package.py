# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Flecsi(CMakePackage, CudaPackage, ROCmPackage):
    """FleCSI is a compile-time configurable framework designed to support
    multi-physics application development. As such, FleCSI attempts to
    provide a very general set of infrastructure design patterns that can
    be specialized and extended to suit the needs of a broad variety of
    solver and data requirements. Current support includes multi-dimensional
    mesh topology, mesh geometry, and mesh adjacency information,
    n-dimensional hashed-tree data structures, graph partitioning
    interfaces,and dependency closures.
    """

    homepage = "http://flecsi.org/"
    git = "https://github.com/flecsi/flecsi.git"
    maintainers("ktsai7", "rbberger")

    tags = ["e4s"]

    version("develop", branch="develop")
    version("2.2.1", tag="v2.2.1", preferred=True)
    version("2.2.0", tag="v2.2.0")
    version("2.1.0", tag="v2.1.0")
    version("2.0.0", tag="v2.0.0")
    version("1.4.1", tag="v1.4.1", submodules=True)
    version(
        "1.4.develop",
        git="https://github.com/laristra/flecsi.git",
        branch="1.4",
        submodules=True,
        deprecated=True,
    )
    version(
        "1.4.2",
        git="https://github.com/laristra/flecsi.git",
        tag="v1.4.2",
        submodules=True,
        deprecated=True,
    )
    version(
        "flecsph",
        git="https://github.com/laristra/flecsi.git",
        branch="stable/flecsph",
        submodules=True,
        deprecated=True,
    )

    variant(
        "backend",
        default="mpi",
        values=("serial", "mpi", "legion", "hpx", "charmpp"),
        description="Backend to use for distributed memory",
        multi=False,
    )
    variant("shared", default=True, description="Build shared libraries")
    variant("flog", default=False, description="Enable flog testing")
    variant("graphviz", default=False, description="Enable GraphViz Support")
    variant("doc", default=False, description="Enable documentation")
    variant("hdf5", default=True, description="Enable HDF5 Support")
    variant(
        "caliper_detail",
        default="none",
        values=("none", "low", "medium", "high"),
        description="Set Caliper Profiling Detail",
        multi=False,
    )
    variant("kokkos", default=False, description="Enable Kokkos Support")
    variant("openmp", default=False, description="Enable OpenMP Support")

    # legacy variants
    variant("coverage", default=False, description="Enable coverage build", when="@:1")
    variant(
        "debug_backend", default=False, description="Build Backend with Debug Mode", when="@:1"
    )
    variant("disable_metis", default=False, description="Disable FindPackageMetis", when="@:1")
    variant("doxygen", default=False, description="Enable doxygen", when="@:1")
    variant("tutorial", default=False, description="Build FleCSI Tutorials", when="@:1")
    variant("flecstan", default=False, description="Build FleCSI Static Analyzer", when="@:1")
    variant("external_cinch", default=False, description="Enable External Cinch", when="@:1")
    variant("unit_tests", default=False, description="Build with Unit Tests Enabled", when="@:1")

    # All Current FleCSI Releases
    for level in ("low", "medium", "high"):
        depends_on("caliper@2.0.1~adiak~libdw", when="@:1 caliper_detail=%s" % level)
        depends_on("caliper", when="@2.0: caliper_detail=%s" % level)
        conflicts("^caliper@2.6", when="@2.0: caliper_detail=%s" % level)
        conflicts("^caliper@2.7", when="@2.0: caliper_detail=%s" % level)

    depends_on("graphviz", when="+graphviz")
    depends_on("hdf5+hl+mpi", when="+hdf5")
    depends_on("metis@5.1.0:")
    depends_on("parmetis@4.0.3:")
    depends_on("boost@1.70.0: cxxstd=17 +program_options")
    depends_on("legion network=gasnet", when="backend=legion")

    # FleCSI@1.x
    depends_on("cmake@3.12:", when="@:1")
    # Requires cinch > 1.0 due to cinchlog installation issue
    depends_on("cinch@1.01:", type="build", when="+external_cinch @:1")
    depends_on("mpi", when="backend=mpi @:1")
    depends_on("mpi", when="backend=legion @:1")
    depends_on("mpi", when="backend=hpx @:1")
    depends_on("legion+shared", when="backend=legion @:1")
    depends_on("legion+hdf5", when="backend=legion +hdf5 @:1")
    depends_on("legion build_type=Debug", when="backend=legion +debug_backend")
    depends_on("legion@cr", when="backend=legion @:1")
    depends_on("hpx@1.4.1 cxxstd=17 malloc=system max_cpu_count=128", when="backend=hpx @:1")
    depends_on("hpx build_type=Debug", when="backend=hpx +debug_backend")
    depends_on("googletest@1.8.1+gmock", when="@:1")
    depends_on("python@3.0:", when="+tutorial @:1")
    depends_on("doxygen", when="+doxygen @:1")
    depends_on("llvm", when="+flecstan @:1")
    depends_on("pfunit@3.0:3", when="@:1")
    depends_on("py-gcovr", when="+coverage @:1")
    depends_on("openmpi+legacylaunchers", when="+unit_tests ^openmpi")

    # FleCSI@2.x
    depends_on("cmake@3.15:", when="@2.0:")
    depends_on("cmake@3.19:", when="@2.2:")
    depends_on("boost +atomic +filesystem +regex +system", when="@2.0:")
    depends_on(
        "boost@1.79.0: cxxstd=17 +program_options +atomic +filesystem +regex +system", when="@2.2:"
    )
    depends_on("kokkos@3.2.00:", when="+kokkos @2.0:")
    depends_on("kokkos +cuda +cuda_constexpr +cuda_lambda", when="+kokkos +cuda @2.0:")
    depends_on("kokkos +rocm", when="+kokkos +rocm @2.0:")
    depends_on("legion@cr", when="backend=legion @2.0:")
    depends_on("legion+shared", when="backend=legion +shared @2.0:")
    depends_on("legion+hdf5", when="backend=legion +hdf5 @2.0:")
    depends_on("legion +kokkos +cuda", when="backend=legion +kokkos +cuda @2.0:")
    depends_on("legion +kokkos +rocm", when="backend=legion +kokkos +rocm @2.0:")
    depends_on("hdf5@1.10.7:", when="backend=legion +hdf5 @2.0:")
    depends_on("hpx@1.8.1: cxxstd=17 malloc=system", when="backend=hpx @2.0:")
    depends_on("mpi", when="@2.0:")
    depends_on("mpich@3.4.1:", when="@2.0: ^mpich")
    depends_on("openmpi@4.1.0:", when="@2.0: ^openmpi")

    # FleCSI 2.2+ documentation dependencies
    depends_on("py-sphinx", when="@2.2: +doc")
    depends_on("py-sphinx-rtd-theme", when="@2.2: +doc")
    depends_on("py-recommonmark", when="@2.2: +doc")
    depends_on("doxygen", when="@2.2: +doc")

    # Propagate cuda_arch requirement to dependencies
    cuda_arch_list = ("60", "70", "75", "80")
    for _flag in cuda_arch_list:
        depends_on("kokkos cuda_arch=" + _flag, when="+cuda+kokkos cuda_arch=" + _flag + " @2.0:")
        depends_on(
            "legion cuda_arch=" + _flag, when="backend=legion +cuda cuda_arch=" + _flag + " @2.0:"
        )

    # Propagate amdgpu_target requirement to dependencies
    for _flag in ROCmPackage.amdgpu_targets:
        depends_on("kokkos amdgpu_target=" + _flag, when="+kokkos +rocm amdgpu_target=" + _flag)
        depends_on(
            "legion amdgpu_target=" + _flag,
            when="backend=legion +rocm amdgpu_target=" + _flag + " @2.0:",
        )

    conflicts("%gcc@:8", when="@2.1:")

    conflicts("+tutorial", when="backend=hpx")
    # FleCSI@2: no longer supports serial or charmpp backends
    conflicts("backend=serial", when="@2.0:")
    conflicts("backend=charmpp", when="@2.0:")
    # FleCSI@:1.4 releases do not support kokkos, omp, cuda, or rocm
    conflicts("+kokkos", when="@:1.4")
    conflicts("+openmp", when="@:1.4")
    conflicts("+cuda", when="@:1.4")
    conflicts("+rocm", when="@:1.4")
    # Unit tests require flog support
    conflicts("+unit_tests", when="~flog")
    # Disallow conduit=none when using legion as a backend
    conflicts("^legion conduit=none", when="backend=legion")
    # Due to overhauls of Legion and Gasnet spackages
    #   flecsi@:1.4 can no longer be built with a usable legion
    conflicts("backend=legion", when="@:1.4")

    def cmake_args(self):
        spec = self.spec

        if spec.satisfies("@2.2:"):
            options = [
                self.define_from_variant("FLECSI_BACKEND", "backend"),
                self.define_from_variant("CALIPER_DETAIL", "caliper_detail"),
                self.define_from_variant("ENABLE_FLOG", "flog"),
                self.define_from_variant("ENABLE_GRAPHVIZ", "graphviz"),
                self.define(
                    "ENABLE_HDF5", "+hdf5" in spec and spec.variants["backend"].value != "hpx"
                ),
                self.define_from_variant("ENABLE_KOKKOS", "kokkos"),
                self.define_from_variant("ENABLE_OPENMP", "openmp"),
                self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
                self.define("ENABLE_UNIT_TESTS", self.run_tests),
                self.define_from_variant("ENABLE_DOCUMENTATION", "doc"),
            ]

            if "+rocm" in self.spec:
                options.append(self.define("CMAKE_CXX_COMPILER", self.spec["hip"].hipcc))
                options.append(self.define("CMAKE_C_COMPILER", self.spec["hip"].hipcc))
        else:
            # kept for supporing version prior to 2.2
            options = [
                self.define_from_variant("FLECSI_RUNTIME_MODEL", "backend"),
                self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
                self.define_from_variant("CALIPER_DETAIL", "caliper_detail"),
                self.define_from_variant("ENABLE_GRAPHVIZ", "graphviz"),
                self.define_from_variant("ENABLE_KOKKOS", "kokkos"),
                self.define_from_variant("ENABLE_OPENMP", "openmp"),
                self.define_from_variant("ENABLE_DOXYGEN", "doxygen"),
                self.define_from_variant("ENABLE_DOCUMENTATION", "doc"),
                self.define_from_variant("ENABLE_COVERAGE_BUILD", "coverage"),
                self.define_from_variant("ENABLE_FLOG", "flog"),
                self.define_from_variant("ENABLE_FLECSIT", "tutorial"),
                self.define_from_variant("ENABLE_FLECSI_TUTORIAL", "tutorial"),
                self.define_from_variant("ENABLE_FLECSTAN", "flecstan"),
                self.define("ENABLE_MPI", spec.variants["backend"].value != "serial"),
                self.define("ENABLE_UNIT_TESTS", self.run_tests or "+unit_tests" in spec),
                self.define(
                    "ENABLE_HDF5", "+hdf5" in spec and spec.variants["backend"].value != "hpx"
                ),
            ]

            if "+external_cinch" in spec:
                options.append(self.define("CINCH_SOURCE_DIR", spec["cinch"].prefix))

            if spec.variants["backend"].value == "hpx":
                options.append(self.define("HPX_IGNORE_CMAKE_BUILD_TYPE_COMPATIBILITY", True))

            if spec.satisfies("@:1"):
                options.append(
                    self.define("ENABLE_CALIPER", spec.variants["caliper_detail"].value != "none")
                )
                options.append(
                    self.define_from_variant("CMAKE_DISABLE_FIND_PACKAGE_METIS", "disable_metis")
                )

        return options
