# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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
    mesh topology, mesh geometry, and mesh adjacency information.
    """

    homepage = "http://flecsi.org/"
    git = "https://github.com/flecsi/flecsi.git"
    maintainers("ktsai7", "rbberger")

    tags = ["e4s"]

    version("develop", branch="develop", deprecated=True)
    version("2.2.1", tag="v2.2.1", commit="84b5b232aebab40610f57387778db80f6c8c84c5")
    version("2.2.0", tag="v2.2.0", commit="dd531ac16c5df124d76e385c6ebe9b9589c2d3ad")
    version("2.1.0", tag="v2.1.0", commit="533df139c267e2a93c268dfe68f9aec55de11cf0")
    version("2.0.0", tag="v2.0.0", commit="5ceebadf75d1c98999ea9e9446926722d061ec22")
    version(
        "1.4.1",
        tag="v1.4.1",
        commit="ab974c3164056e6c406917c8ca771ffd43c5a031",
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
    variant("flog", default=False, description="Enable logging support")
    variant("graphviz", default=False, description="Enable GraphViz Support")
    variant("doc", default=False, description="Enable documentation", when="@2.2:")
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
    depends_on("boost@1.70.0: cxxstd=17 +program_options +stacktrace")

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
    depends_on("legion@cr-20191217", when="backend=legion @:1")
    depends_on("hpx@1.4.1 cxxstd=17 malloc=system max_cpu_count=128", when="backend=hpx @:1")
    depends_on("hpx build_type=Debug", when="backend=hpx +debug_backend")
    depends_on("googletest@1.8.1+gmock", when="@:1")
    depends_on("python@3.0:", when="+tutorial @:1")
    depends_on("doxygen", when="+doxygen @:1")
    depends_on("llvm", when="+flecstan @:1")
    depends_on("pfunit@3.0:3", when="@:1")
    depends_on("py-gcovr", when="+coverage @:1")
    depends_on("openmpi+legacylaunchers", when="+unit_tests ^[virtuals=mpi] openmpi")

    # FleCSI@2.x
    depends_on("cmake@3.15:", when="@2.0:")
    depends_on("cmake@3.19:", when="@2.2:")
    depends_on("boost +atomic +filesystem +regex +system", when="@2.0:2.2.1")
    depends_on("boost@1.79.0:", when="@2.2:")
    depends_on("kokkos@3.2.00:", when="+kokkos @2.0:")
    depends_on("kokkos +cuda +cuda_constexpr +cuda_lambda", when="+kokkos +cuda @2.0:")
    depends_on("kokkos +rocm", when="+kokkos +rocm @2.0:")
    depends_on("kokkos +openmp", when="+kokkos +openmp @2.0:")
    depends_on("legion@cr-20210122", when="backend=legion @2.0:2.2.1")
    depends_on("legion@cr-20230307", when="backend=legion @2.2.0:2.2.1")
    depends_on("legion@24.03.0:", when="backend=legion @2.2.2:")
    depends_on("legion+shared", when="backend=legion +shared @2.0:")
    depends_on("legion+hdf5", when="backend=legion +hdf5 @2.0:")
    depends_on("legion+kokkos", when="backend=legion +kokkos @2.0:")
    depends_on("legion+openmp", when="backend=legion +openmp @2.0:")
    depends_on("legion+cuda", when="backend=legion +cuda @2.0:")
    depends_on("legion+rocm", when="backend=legion +rocm @2.0:")
    depends_on("hdf5@1.10.7:", when="backend=legion +hdf5 @2.0:")
    depends_on("hpx@1.9.1: cxxstd=17 malloc=system", when="backend=hpx @2.0:")
    depends_on("mpi", when="@2.0:")
    depends_on("mpich@3.4.1:", when="@2.0: ^[virtuals=mpi] mpich")
    depends_on("openmpi@4.1.0:", when="@2.0: ^[virtuals=mpi] openmpi")

    # FleCSI 2.2+ documentation dependencies
    depends_on("py-sphinx", when="+doc")
    depends_on("py-sphinx-rtd-theme", when="+doc")
    depends_on("py-recommonmark", when="+doc")
    depends_on("doxygen", when="+doc")
    depends_on("graphviz", when="+doc")

    # Propagate cuda_arch requirement to dependencies
    for _flag in CudaPackage.cuda_arch_values:
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

    requires("%gcc@9:", when="@2: %gcc", msg="Version 9 or newer of GNU compilers required!")

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
    conflicts("+hdf5", when="@2: backend=hpx", msg="HPX backend doesn't support HDF5")

    def cmake_args(self):
        spec = self.spec

        if spec.satisfies("@2.2:"):
            options = [
                self.define_from_variant("FLECSI_BACKEND", "backend"),
                self.define_from_variant("CALIPER_DETAIL", "caliper_detail"),
                self.define_from_variant("ENABLE_FLOG", "flog"),
                self.define_from_variant("ENABLE_GRAPHVIZ", "graphviz"),
                self.define_from_variant("ENABLE_HDF5", "hdf5"),
                self.define_from_variant("ENABLE_KOKKOS", "kokkos"),
                self.define_from_variant("ENABLE_OPENMP", "openmp"),
                self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
                self.define("ENABLE_UNIT_TESTS", self.run_tests),
                self.define_from_variant("ENABLE_DOCUMENTATION", "doc"),
            ]

            if "+rocm" in self.spec:
                options.append(self.define("CMAKE_CXX_COMPILER", self.spec["hip"].hipcc))
                options.append(self.define("CMAKE_C_COMPILER", self.spec["hip"].hipcc))
                if "backend=legion" in self.spec:
                    # CMake pulled in via find_package(Legion) won't work without this
                    options.append(self.define("HIP_PATH", "{0}/hip".format(spec["hip"].prefix)))
            elif "+kokkos" in self.spec:
                options.append(self.define("CMAKE_CXX_COMPILER", self.spec["kokkos"].kokkos_cxx))
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
                self.define_from_variant("ENABLE_COVERAGE_BUILD", "coverage"),
                self.define_from_variant("ENABLE_FLOG", "flog"),
                self.define_from_variant("ENABLE_FLECSIT", "tutorial"),
                self.define_from_variant("ENABLE_FLECSI_TUTORIAL", "tutorial"),
                self.define_from_variant("ENABLE_FLECSTAN", "flecstan"),
                self.define("ENABLE_MPI", spec.variants["backend"].value != "serial"),
                self.define("ENABLE_UNIT_TESTS", self.run_tests or "+unit_tests" in spec),
                self.define_from_variant("ENABLE_HDF5", "hdf5"),
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
