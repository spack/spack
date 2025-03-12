# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.python import PythonPipBuilder
from spack.package import *


class Warpx(CMakePackage, PythonExtension):
    """WarpX is an advanced electromagnetic Particle-In-Cell code. It supports
    many features including Perfectly-Matched Layers (PML) and mesh refinement.

    In addition, WarpX is a highly-parallel and highly-optimized code and
    features hybrid GPU/OpenMP/MPI parallelization and load balancing capabilities.
    """

    homepage = "https://ecp-warpx.github.io"
    url = "https://github.com/ECP-WarpX/WarpX/archive/refs/tags/25.03.tar.gz"
    git = "https://github.com/ECP-WarpX/WarpX.git"

    maintainers("ax3l", "dpgrote", "EZoni", "RemiLehe")
    tags = ["e4s", "ecp"]

    license("BSD-3-Clause-LBNL")

    # NOTE: if you update the versions here, also see py-warpx
    version("develop", branch="development")
    version("25.03", sha256="18155ff67b036a00db2a25303058316167192a81cfe6dc1dec65fdef0b6d9903")
    with default_args(deprecated=True):
        version("25.02", sha256="7bdea9c1e94f82dbc3565f14f6b6ad7658a639217a10a6cf08c05a16aa26266f")
        version("24.10", sha256="73b486b5fc561d97773fe95bb82751b9085aa8dfe27b4e2f285d646396b41323")
        version("24.08", sha256="081b0d803d7b2b491626ba36e87e867b1fd1d20ddf0dee9c6ed4ff84f7d37553")
        version("23.08", sha256="22b9ad39c89c3fae81b1ed49abd72f698fbc79d8ac3b8dd733fd02185c0fdf63")
        version("23.07", sha256="eab91672191d7bf521cda40f2deb71a144da452b35245567b14873938f97497e")
        version("23.06", sha256="9bbdcbfae3d7e87cd4457a0debd840897e9a9d15e14eaad4be8c8e16e13adca2")
        version("23.05", sha256="fa4f6d8d0537057313bb657c60d5fd91ae6219d3de95d446282f1ad47eeda863")
        version("23.04", sha256="90462a91106db8e241758aeb8aabdf3e217c9e3d2c531d6d30f0d03fd3ef789c")
        version("23.03", sha256="26e79f8c7f0480b5f795d87ec2663e553b357894fc4b591c8e70d64bfbcb72a4")
        version("23.02", sha256="596189e5cebb06e8e58a587423566db536f4ac3691d01db8d11f5503f1e7e35e")
        version("23.01", sha256="ed0536ae5a75df4b93c275c6839a210fba61c9524a50ec6217c44d5ac83776b3")
        version("22.12", sha256="bdd0a9ec909a5ac00f288bb4ab5193136b460e39e570ecb37d3d5d742b7e67bf")
        version("22.11", sha256="03c580bcd0cf7b99a81b9ef09d14172c96672c7fb028a0ed6728b3cc9ec207e7")
        version("22.10", sha256="736747184eaae65fb1bbeb6867b890c90b233132bc185d85ea605525637e7c53")
        version("22.09", sha256="0dc7076bad1c46045abd812729fa650bc4f3d17fdfded6666cbaf06da70f09d7")
        version("22.08", sha256="95930c4f4fc239dfe4ed36b1023dd3768637ad37ff746bb33cf05231ca08ee7a")
        version("22.07", sha256="7d91305f8b54b36acf2359daec5a94e154e2a8d7cbae97429ed8e93f7c5ea661")
        version("22.06", sha256="faa6550d7dd48fc64d4b4d67f583d34209c020bf4f026d10feb7c9b224caa208")
        version("22.05", sha256="be97d695a425cfb0ecd3689a0b9706575b7b48ce1c73c39d4ea3abd616b15ad7")
        version("22.04", sha256="ff6e3a379fafb76e311b2f48089da6b1ab328c5b52eccd347c41cce59d0441ed")
        version("22.03", sha256="808a9f43514ee40fa4fa9ab5bf0ed11219ab6f9320eb414bb4f043fab112f7a0")
        version("22.02", sha256="3179c54481c5dabde77a4e9a670bb97b599cecc617ad30f32ab3177559f67ffe")
        version("22.01", sha256="73a65c1465eca80f0db2dab4347c22ddf68ad196e3bd0ccc0861d782f13b7388")
        # 22.01+ requires C++17 or newer
        version("21.12", sha256="3dd96d36db531f518cfec631bec243029fe63e1084b8cf7e8e75be50ebbdc794")
        version("21.11", sha256="03727c21ee350fdc63057d4eebbff142928d74481f2234a8c3821cf338bfa4a0")
        version("21.10", sha256="c35a98b1bd349cb944296c02d6e0602b6b7e33d1008207dd0d041a75cfb971e9")
        version("21.09", sha256="0b20c5d7f13448f01115f68f131a3721e037ad9fab06aa3c24530bc48859c9eb")
        version("21.08", sha256="5e61e4ec5a8605aa4fb89d49feba4a42d7d3f627745d4c85faab3657baf56011")
        version("21.07", sha256="fe566f3de8d5b17a720e084d244c6617c87523b7d80756cbb5850df6e8100f5f")
        version("21.06", sha256="246fb2c2bdb1dad347550c48e375326bc7bdeec0496c113c1057d2721a9ffd14")
        version("21.05", sha256="16a206e898b22ace07c8dc9ea70af7f6f6f91a7a2e42c392fd15eb223faa1597")
        version("21.04", sha256="13b13aebb25f43b7239743312dc9bb96bb365b72a99eb3c64492ae38f5141cff")
        # 20.01+ requires C++14 or newer

    variant("app", default=True, description="Build the WarpX executable application")
    variant("ascent", default=False, description="Enable Ascent in situ visualization")
    variant(
        "catalyst",
        default=False,
        description="Enable Catalyst2 in situ visualization",
        when="@24.09:",
    )
    variant("sensei", default=False, description="Enable SENSEI in situ visualization")
    variant(
        "compute",
        default="omp",
        values=("omp", "cuda", "hip", "sycl", "noacc"),
        multi=False,
        description="On-node, accelerated computing backend",
    )
    variant(
        "dims",
        default="3",
        values=("1", "2", "3", "rz"),
        multi=False,
        description="Number of spatial dimensions",
        when="@:23.05",
    )
    variant(
        "dims",
        default="1,2,rz,3",
        values=("1", "2", "3", "rz"),
        multi=True,
        description="Number of spatial dimensions",
        when="@23.06:",
    )
    variant("eb", default=True, description="Embedded boundary support", when="@24.10:")
    variant("eb", default=False, description="Embedded boundary support", when="@:24.09")
    # Spack defaults to False but pybind11 defaults to True (and IPO is highly
    # encouraged to be used)
    variant(
        "python_ipo",
        default=True,
        description="CMake interprocedural optimization for Python bindings (recommended)",
    )
    variant("lib", default=True, description="Build WarpX as a shared library")
    variant("mpi", default=True, description="Enable MPI support")
    variant(
        "mpithreadmultiple",
        default=True,
        description="MPI thread-multiple support, i.e. for async_io",
    )
    variant("openpmd", default=True, description="Enable openPMD I/O")
    variant(
        "precision",
        default="double",
        values=("single", "double"),
        multi=False,
        description="Floating point precision (single/double)",
    )
    variant("fft", default=True, description="Enable support for FFT-based solvers")
    variant("python", default=False, description="Enable Python bindings")
    variant("qed", default=True, description="Enable QED support")
    variant("qedtablegen", default=False, description="QED table generation support")
    variant("shared", default=True, description="Build a shared version of the library")
    variant("tprof", default=True, description="Enable tiny profiling features")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    for v in ["25.03", "25.02", "24.10", "24.08", "develop"]:
        depends_on(
            f"amrex@{v} build_system=cmake +linear_solvers +pic +particles +shared +tiny_profile",
            when=f"@{v}",
            type=("build", "link"),
        )
        depends_on("py-amrex@{0}".format(v), when="@{0} +python".format(v), type=("build", "run"))

    depends_on("boost@1.66.0: +math", when="+qedtablegen")
    depends_on("cmake@3.15.0:", type="build")
    depends_on("cmake@3.18.0:", type="build", when="@22.01:")
    depends_on("cmake@3.20.0:", type="build", when="@22.08:")
    depends_on("cmake@3.24.0:", type="build", when="@24.09:")
    with when("+ascent"):
        depends_on("ascent", when="+ascent")
        depends_on("ascent +cuda", when="+ascent compute=cuda")
        depends_on("ascent +mpi", when="+ascent +mpi")
        depends_on("amrex +ascent +conduit")
    with when("+catalyst"):
        depends_on("libcatalyst@2.0: +conduit")
        depends_on("libcatalyst +mpi", when="+mpi")
        depends_on("amrex +catalyst +conduit")
    with when("dims=1"):
        depends_on("amrex dimensions=1")
    with when("dims=2"):
        depends_on("amrex dimensions=2")
    with when("dims=rz"):
        depends_on("amrex dimensions=2")
    with when("dims=3"):
        depends_on("amrex dimensions=3")
    with when("+eb"):
        depends_on("amrex +eb")
    with when("+fft"):
        depends_on("amrex +fft", when="@24.11:")
    depends_on("mpi", when="+mpi")
    with when("+mpi"):
        depends_on("amrex +mpi")
        depends_on("py-amrex +mpi", when="+python")
    with when("~mpi"):
        depends_on("amrex ~mpi")
        depends_on("py-amrex ~mpi", when="~python")
    with when("precision=single"):
        depends_on("amrex precision=single")
    with when("precision=double"):
        depends_on("amrex precision=double")
    depends_on("py-pybind11@2.12.0:", when="@24.04: +python", type=("build", "link"))
    depends_on("sensei@4.0.0:", when="@22.07: +sensei")
    with when("compute=cuda"):
        depends_on("amrex +cuda")
        depends_on("cuda@9.2.88:")
        depends_on("cuda@11.0:", when="@22.01:")
    with when("compute=hip"):
        depends_on("amrex +rocm")
        depends_on("rocfft", when="+fft")
        depends_on("rocprim")
        depends_on("rocrand")
    with when("compute=noacc"):
        depends_on("amrex ~cuda ~openmp ~rocm ~sycl")
        with when("+fft"):
            depends_on("fftw@3: ~mpi", when="~mpi")
            depends_on("fftw@3: +mpi", when="+mpi")
            depends_on("pkgconfig", type="build")
    with when("compute=omp"):
        depends_on("amrex +openmp")
        depends_on("llvm-openmp", when="%apple-clang")
        with when("+fft"):
            depends_on("fftw@3: +openmp")
            depends_on("fftw ~mpi", when="~mpi")
            depends_on("fftw +mpi", when="+mpi")
            depends_on("pkgconfig", type="build")
    with when("+fft dims=rz"):
        depends_on("lapackpp")
        depends_on("blaspp")
        depends_on("blaspp +cuda", when="compute=cuda")
    with when("+openpmd"):
        depends_on("openpmd-api@0.13.1:")
        depends_on("openpmd-api@0.14.2:", when="@21.09:")
        depends_on("openpmd-api@0.15.1:", when="@23.05:")
        depends_on("openpmd-api@0.16.1:", when="@25.02:")
        depends_on("openpmd-api ~mpi", when="~mpi")
        depends_on("openpmd-api +mpi", when="+mpi")

    # Python bindings
    # note: in Spack, we only need the cmake package, not py-cmake
    with when("+python"):
        extends("python")
        depends_on("python@3.8:", type=("build", "run"))
        depends_on("py-numpy@1.15.0:", type=("build", "run"))
        depends_on("py-mpi4py@2.1.0:", type=("build", "run"), when="+mpi")
        depends_on("py-periodictable@1.5:1", type=("build", "run"))
        depends_on("py-picmistandard@0.28.0", type=("build", "run"), when="@23.11:24.07")
        depends_on("py-picmistandard@0.29.0", type=("build", "run"), when="@24.08")
        depends_on("py-picmistandard@0.30.0", type=("build", "run"), when="@24.09:24.12")
        depends_on("py-picmistandard@0.33.0", type=("build", "run"), when="@25.01:")
        depends_on("py-pip@23:", type="build")
        depends_on("py-setuptools@42:", type="build")
        depends_on("py-pybind11@2.12.0:", type=("build", "link"))
        depends_on("py-wheel@0.40:", type="build")

    conflicts("+python", when="@:24.04", msg="Python bindings only supported in 24.04+")
    conflicts("dims=1", when="@:21.12", msg="WarpX 1D support starts in 22.01+")
    conflicts("~qed +qedtablegen", msg="WarpX PICSAR QED table generation needs +qed")
    conflicts(
        "compute=sycl",
        when="+fft",
        msg="WarpX spectral solvers are not yet tested with SYCL " '(use "warpx ~fft")',
    )
    conflicts("+sensei", when="@:22.06", msg="WarpX supports SENSEI 4.0+ with 22.07 and newer")

    # The symbolic aliases for our +lib target were missing in the install
    # location
    # https://github.com/ECP-WarpX/WarpX/pull/2626
    patch(
        "https://github.com/ECP-WarpX/WarpX/pull/2626.patch?full_index=1",
        sha256="a431d4664049d6dcb6454166d6a948d8069322a111816ca5ce01553800607544",
        when="@21.12",
    )

    # Workaround for AMReX<=22.06 no-MPI Gather
    # https://github.com/ECP-WarpX/WarpX/pull/3134
    # https://github.com/AMReX-Codes/amrex/pull/2793
    patch(
        "https://github.com/ECP-WarpX/WarpX/pull/3134.patch?full_index=1",
        sha256="b786ce64a3c2c2b96ff2e635f0ee48532e4ae7ad9637dbf03f11c0768c290690",
        when="@22.02:22.05",
    )

    # Forgot to install ABLASTR library
    # https://github.com/ECP-WarpX/WarpX/pull/3141
    patch(
        "https://github.com/ECP-WarpX/WarpX/pull/3141.patch?full_index=1",
        sha256="dab6fb44556ee1fd466a4cb0e20f89bde1ce445c9a51a2c0f59d1740863b5e7d",
        when="@22.04,22.05",
    )

    # Fix failing 1D CUDA build
    # https://github.com/ECP-WarpX/WarpX/pull/3162
    patch(
        "https://github.com/ECP-WarpX/WarpX/pull/3162.patch?full_index=1",
        sha256="0ae573d1390ed8063f84e3402d30d34e522e65dc5dfeea3d07e165127ab373e9",
        when="@22.06",
    )

    def cmake_args(self):
        spec = self.spec

        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            "-DCMAKE_INSTALL_LIBDIR=lib",
            # variants
            self.define_from_variant("WarpX_APP", "app"),
            self.define_from_variant("WarpX_ASCENT", "ascent"),
            self.define_from_variant("WarpX_CATALYST", "catalyst"),
            self.define_from_variant("WarpX_SENSEI", "sensei"),
            "-DWarpX_COMPUTE={0}".format(spec.variants["compute"].value.upper()),
            "-DWarpX_DIMS={0}".format(";".join(spec.variants["dims"].value).upper()),
            self.define_from_variant("WarpX_EB", "eb"),
            self.define_from_variant("WarpX_LIB", "lib"),
            self.define_from_variant("WarpX_MPI", "mpi"),
            self.define_from_variant("WarpX_MPI_THREAD_MULTIPLE", "mpithreadmultiple"),
            self.define_from_variant("WarpX_OPENPMD", "openpmd"),
            "-DWarpX_PRECISION={0}".format(spec.variants["precision"].value.upper()),
            self.define_from_variant("WarpX_PYTHON", "python"),
            self.define_from_variant("WarpX_QED", "qed"),
            self.define_from_variant("WarpX_QED_TABLE_GEN", "qedtablegen"),
        ]

        if spec.satisfies("@24.08:"):
            args.append("-DWarpX_amrex_internal=OFF")
            args.append(self.define_from_variant("WarpX_FFT", "fft"))
        else:
            args.append(self.define_from_variant("WarpX_PSATD", "fft"))

        # FindMPI needs an extra hint sometimes, particularly on cray systems
        if "+mpi" in spec:
            args.append(self.define("MPI_C_COMPILER", spec["mpi"].mpicc))
            args.append(self.define("MPI_CXX_COMPILER", spec["mpi"].mpicxx))

        if "+openpmd" in spec:
            args.append("-DWarpX_openpmd_internal=OFF")

        if "+python" in spec:
            if spec.satisfies("@24.08:"):
                args.append("-DWarpX_pyamrex_internal=OFF")
                args.append("-DWarpX_pybind11_internal=OFF")
                args.append(self.define_from_variant("WarpX_PYTHON_IPO", "python_ipo"))

        # Work-around for SENSEI 4.0: wrong install location for CMake config
        #   https://github.com/SENSEI-insitu/SENSEI/issues/79
        if "+sensei" in spec:
            args.append(self.define("SENSEI_DIR", spec["sensei"].prefix.lib.cmake))

        # WarpX uses CCache by default, interfering with Spack wrappers
        ccache_var = "CCACHE_PROGRAM" if spec.satisfies("@:24.01") else "WarpX_CCACHE"
        args.append(self.define(ccache_var, False))

        return args

    phases = ("cmake", "build", "install", "pip_install_nodeps")
    build_targets = ["all"]
    with when("+python"):
        build_targets += ["pip_wheel"]

    def pip_install_nodeps(self, spec, prefix):
        """Install everything from build directory."""
        pip = spec["python"].command
        pip.add_default_arg("-m", "pip")

        args = PythonPipBuilder.std_args(self) + [
            f"--prefix={prefix}",
            "--find-links=warpx-whl",
            "pywarpx",
        ]

        with working_dir(self.build_directory):
            pip(*args)

        # todo: from PythonPipBuilder
        # ....execute_install_time_tests()

    @property
    def libs(self):
        libsuffix = {"1": "1d", "2": "2d", "3": "3d", "rz": "rz"}
        libs = []
        for dim in self.spec.variants["dims"].value:
            libs += find_libraries(
                ["libwarpx." + libsuffix[dim]], root=self.prefix, recursive=True, shared=True
            )
            libs += find_libraries(
                ["libablastr"],
                root=self.prefix,
                recursive=True,
                shared=self.spec.variants["shared"],
            )
        return libs

    # WarpX has many examples to serve as a suitable smoke check. One
    # that is typical was chosen here
    examples_src_dir = "Examples/Physics_applications/laser_acceleration/"

    def _get_input_options(self, dim, post_install):
        spec = self.spec
        examples_dir = join_path(
            install_test_root(self) if post_install else self.stage.source_path,
            self.examples_src_dir,
        )
        if spec.satisfies("@:24.09"):
            inputs_nD = {"1": "inputs_1d", "2": "inputs_2d", "3": "inputs_3d", "rz": "inputs_rz"}
            if spec.satisfies("@:21.12"):
                inputs_nD["rz"] = "inputs_2d_rz"
        else:
            inputs_nD = {
                "1": "inputs_test_1d_laser_acceleration",
                "2": "inputs_base_2d",
                "3": "inputs_base_3d",
                "rz": "inputs_base_rz",
            }
        inputs = join_path(examples_dir, inputs_nD[dim])

        cli_args = [inputs, "max_step=50", "diag1.intervals=10"]
        # test openPMD output if compiled in
        if "+openpmd" in spec:
            cli_args.append("diag1.format=openpmd")
            # RZ: New openPMD thetaMode output
            if dim == "rz" and spec.satisfies("@22.04:"):
                cli_args.append("diag1.fields_to_plot=Er Et Ez Br Bt Bz jr jt jz rho")
        return cli_args

    def check(self):
        """Checks after the build phase"""
        spec = self.spec
        if "+app" not in spec:
            print("WarpX check skipped: requires variant +app")
            return

        with working_dir("spack-check", create=True):
            for dim in spec.variants["dims"].value:
                cli_args = self._get_input_options(dim, False)
                exe_nD = {"1": "warpx.1d", "2": "warpx.2d", "3": "warpx.3d", "rz": "warpx.rz"}
                warpx = Executable(join_path(self.build_directory, "bin/" + exe_nD[dim]))
                warpx(*cli_args)

    @run_after("install")
    def copy_test_sources(self):
        """Copy the example input files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        cache_extra_test_sources(self, [self.examples_src_dir])

    # TODO: remove installed static ablastr lib
    #       (if build as static lib - Spack default is shared)
    #    @run_after("install")
    #    def remove_unwanted_library(self):
    #        ... libablastr_{1d,2d,3d,rz}.a ...

    def run_warpx(self, dim):
        """Perform smoke tests on the installed package."""
        if "+app" not in self.spec:
            raise SkipTest("Package must be installed with +app")
        if dim not in self.spec.variants["dims"].value:
            raise SkipTest(f"Package must be installed with {dim} in dims")
        dim_arg = f"{dim}d" if dim.isdigit() else dim
        if self.spec.satisfies("@:23.05") and not dim.isdigit():
            dim_arg = dim_arg.upper()
        exe = find(self.prefix.bin, f"warpx.{dim_arg}.*", recursive=False)[0]
        cli_args = self._get_input_options(dim, True)
        warpx = which(exe)
        warpx(*cli_args)

    def test_warpx_1d(self):
        """Run warpx 1d test"""
        self.run_warpx("1")

    def test_warpx_2d(self):
        """Run warpx 2d test"""
        self.run_warpx("2")

    def test_warpx_3d(self):
        """Run warpx 3d test"""
        self.run_warpx("3")

    def test_warpx_rz(self):
        """Run warpx rz test"""
        self.run_warpx("rz")
