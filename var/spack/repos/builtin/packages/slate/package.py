# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Slate(CMakePackage, CudaPackage, ROCmPackage):
    """The Software for Linear Algebra Targeting Exascale (SLATE) project is
    to provide fundamental dense linear algebra capabilities to the US
    Department of Energy and to the high-performance computing (HPC) community
    at large. To this end, SLATE will provide basic dense matrix operations
    (e.g., matrix multiplication, rank-k update, triangular solve), linear
    systems solvers, least square solvers, singular value and eigenvalue
    solvers."""

    homepage = "https://icl.utk.edu/slate/"
    git = "https://github.com/icl-utk-edu/slate"
    url = "https://github.com/icl-utk-edu/slate/releases/download/v2022.07.00/slate-2022.07.00.tar.gz"
    maintainers("G-Ragghianti", "mgates3")

    tags = ["e4s"]
    test_requires_compiler = True

    version("master", branch="master")
    version(
        "2022.07.00", sha256="176db81aef44b1d498a37c67b30aff88d4025770c9200e19ceebd416e4101327"
    )
    version(
        "2022.06.00", sha256="4da23f3c3c51fde65120f80df2b2f703aee1910389c08f971804aa77d11ac027"
    )
    version(
        "2022.05.00", sha256="960f61ec2a4e1fa5504e3e4bdd8f62e607936f27a8fd66f340d15119706df588"
    )
    version(
        "2021.05.02", sha256="29667a9e869e41fbc22af1ae2bcd425d79b4094bbb3f21c411888e7adc5d12e3"
    )
    version(
        "2021.05.01", sha256="d9db2595f305eb5b1b49a77cc8e8c8e43c3faab94ed910d8387c221183654218"
    )
    version(
        "2020.10.00", sha256="ff58840cdbae2991d100dfbaf3ef2f133fc2f43fc05f207dc5e38a41137882ab"
    )

    variant(
        "mpi", default=True, description="Build with MPI support (without MPI is experimental)."
    )
    variant("openmp", default=True, description="Build with OpenMP support.")
    variant("shared", default=True, description="Build shared library")

    # The runtime dependency on cmake is needed by the stand-alone tests (spack test).
    depends_on("cmake", type="run")

    depends_on("mpi", when="+mpi")
    depends_on("blas")
    depends_on("blaspp ~cuda", when="~cuda")
    depends_on("blaspp +cuda", when="+cuda")
    depends_on("blaspp ~rocm", when="~rocm")
    depends_on("lapackpp ~cuda", when="~cuda")
    depends_on("lapackpp +cuda", when="+cuda")
    depends_on("lapackpp ~rocm", when="~rocm")
    for val in CudaPackage.cuda_arch_values:
        depends_on("blaspp +cuda cuda_arch=%s" % val, when="cuda_arch=%s" % val)
        depends_on("lapackpp +cuda cuda_arch=%s" % val, when="cuda_arch=%s" % val)
    for val in ROCmPackage.amdgpu_targets:
        depends_on("blaspp +rocm amdgpu_target=%s" % val, when="amdgpu_target=%s" % val)
        depends_on("lapackpp +rocm amdgpu_target=%s" % val, when="amdgpu_target=%s" % val)
    depends_on("lapackpp@2022.07.00", when="@2022.07.00:")
    depends_on("lapackpp@2022.05.00:", when="@2022.05.00:")
    depends_on("lapackpp@2021.04.00:", when="@2021.05.01:")
    depends_on("lapackpp@2020.10.02", when="@2020.10.00")
    depends_on("lapackpp@master", when="@master")
    depends_on("scalapack", type="test")
    depends_on("hipify-clang", when="@:2021.05.02 +rocm ^hip@5:")

    cpp_17_msg = "Requires C++17 compiler support"
    conflicts("%gcc@:5", msg=cpp_17_msg)
    conflicts("%xl", msg=cpp_17_msg)
    conflicts("%xl_r", msg=cpp_17_msg)
    conflicts("%intel@19:", msg="Does not currently build with icpc >= 2019")
    conflicts(
        "+rocm", when="@:2020.10.00", msg="ROCm support requires SLATE 2021.05.01 or greater"
    )
    conflicts("+rocm", when="+cuda", msg="SLATE only supports one GPU backend at a time")

    def cmake_args(self):
        spec = self.spec
        backend_config = "-Duse_cuda=%s" % ("+cuda" in spec)
        if self.version >= Version("2021.05.01"):
            backend = "none"
            if "+cuda" in spec:
                backend = "cuda"
            if "+rocm" in spec:
                backend = "hip"
            backend_config = "-Dgpu_backend=%s" % backend

        config = [
            "-Dbuild_tests=%s" % self.run_tests,
            "-Duse_openmp=%s" % ("+openmp" in spec),
            "-DBUILD_SHARED_LIBS=%s" % ("+shared" in spec),
            backend_config,
            "-Duse_mpi=%s" % ("+mpi" in spec),
        ]
        if self.run_tests:
            config.append("-DSCALAPACK_LIBRARIES=%s" % spec["scalapack"].libs.joined(";"))
        return config

    @run_after("install")
    def cache_test_sources(self):
        if self.spec.satisfies("@2020.10.00"):
            return
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        self.cache_extra_test_sources(["examples"])

    def mpi_launcher(self):
        searchpath = [self.spec["mpi"].prefix.bin]
        try:
            searchpath.insert(0, self.spec["slurm"].prefix.bin)
        except KeyError:
            print("Slurm not found, ignoring.")
        commands = ["srun", "mpirun", "mpiexec"]
        return which(*commands, path=searchpath) or which(*commands)

    def test(self):
        if self.spec.satisfies("@2020.10.00") or "+mpi" not in self.spec:
            print("Skipping: stand-alone tests")
            return

        test_dir = join_path(self.test_suite.current_test_cache_dir, "examples", "build")
        with working_dir(test_dir, create=True):
            cmake_bin = join_path(self.spec["cmake"].prefix.bin, "cmake")
            deps = "blaspp lapackpp mpi"
            if self.spec.satisfies("+rocm"):
                deps += " rocblas hip llvm-amdgpu comgr hsa-rocr-dev rocsolver"
            prefixes = ";".join([self.spec[x].prefix for x in deps.split()])
            self.run_test(cmake_bin, ["-DCMAKE_PREFIX_PATH=" + prefixes, ".."])
            make()
            test_args = ["-n", "4", "./ex05_blas"]
            launcher = self.mpi_launcher()
            if not launcher:
                raise RuntimeError("Cannot run tests due to absence of MPI launcher")
            self.run_test(launcher.command, test_args, purpose="SLATE smoke test")
            make("clean")
