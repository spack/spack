# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil

from llnl.util import tty

from spack.package import *

class Amber(CMakePackage, CudaPackage):
    """Amber is a suite of biomolecular simulation programs together
    with Amber tools.

    A manual download is required for Ambers. Spack will search your current
    directory for the download files. Alternatively, add the files to a mirror
    so that Spack can find them. For instructions on how to set up a mirror, see
    https://spack.readthedocs.io/en/latest/mirrors.html

    Note: Only certain versions of ambertools are compatible with amber.
    Only the latter version of ambertools for each amber version is supported.
    """

    homepage = "https://ambermd.org/"
    url = "file://{0}/Amber18.tar.bz2".format(os.getcwd())
    manual_download = True

    maintainers("hseara")


    version("22", sha256="3c887ccbad690fc76ff0b120a3448eae023c08e76582aac07900d4a9708ebd16")
    version("20", sha256="a4c53639441c8cc85adee397933d07856cc4a723c82c6bea585cd76c197ead75")
    version("18", sha256="2060897c0b11576082d523fb63a51ba701bc7519ff7be3d299d5ec56e8e6e277")
    version(
        "16",
        sha256="3b7ef281fd3c46282a51b6a6deed9ed174a1f6d468002649d84bfc8a2577ae5d",
        deprecated=True,
    )

    resources = {
        # [version amber, version ambertools , sha256sum]
        "22": ("22", "1571d4e0f7d45b2a71dce5999fa875aea8c90ee219eb218d7916bf30ea229121"),
        "20": ("21", "f55fa930598d5a8e9749e8a22d1f25cab7fcf911d98570e35365dd7f262aaafd"),
        # '20': ('20', 'b1e1f8f277c54e88abc9f590e788bbb2f7a49bcff5e8d8a6eacfaf332a4890f9'),
        "18": ("19", "0c86937904854b64e4831e047851f504ec45b42e593db4ded92c1bee5973e699"),
        "16": ("16", "7b876afe566e9dd7eb6a5aa952a955649044360f15c1f5d4d91ba7f41f3105fa"),
    }
    for ver, (ambertools_ver, ambertools_checksum) in resources.items():
        resource(
            when="@{0}".format(ver),
            name="AmberTools",
            url="file://{0}/AmberTools{1}.tar.bz2".format(os.getcwd(), ambertools_ver),
            sha256=ambertools_checksum,
            destination="",
            placement="ambertools_tmpdir"
        )


    depends_on("cmake", type="build")


    patches = [
        ("20", "1", "10780cb91a022b49ffdd7b1e2bf4a572fa4edb7745f0fc4e5d93b158d6168e42"),
        ("20", "2", "9c973e3f8f33a271d60787e8862901e8f69e94e7d80cda1695f7fad7bc396093"),
        ("20", "3", "acb359dc9b1bcff7e0f1965baa9f3f3dc18eeae99c49f1103c1e2986c0bbeed8"),
        ("20", "4", "fd93c74f5ec80689023648cdd12b2c5fb21a3898c81ebc3fa256ef244932562a"),
        ("20", "5", "8e46d5be28c002f560050a71f4851b01ef45a3eb66ac90d7e23553fae1370e68"),
        ("20", "6", "8cf9707b3d08ad9242326f02d1861831ad782c9bfb0c46e7b1f0d4640571d5c1"),
        ("20", "7", "143b6a09f774aeae8b002afffb00839212020139a11873a3a1a34d4a63fa995d"),
        ("20", "8", "a6fc6d5c8ba0aad3a8afe44d1539cc299ef78ab53721e28244198fd5425d14ad"),
        ("20", "9", "5ce6b534bab869b1e9bfefa353d7f578750e54fa72c8c9d74ddf129d993e78cf"),
        ("20", "10", "76a683435be7cbb860f5bd26f09a0548c2e77c5a481fc6d64b55a3a443ce481d"),
        ("20", "11", "f40b3612bd3e59efa2fa1ec06ed6fd92446ee0f1d5d99d0f7796f66b18e64060"),
        ("20", "12", "194119aed03f80677c4bab78a20fc09b0b3dc17c41a57c5eb3c912b2d73b18ab"),
        ("18", "1", "3cefac9a24ece99176d5d2d58fea2722de3e235be5138a128428b9260fe922ad"),
        ("18", "2", "3a0707a9a59dcbffa765dcf87b68001450095c51b96ec39d21260ba548a2f66a"),
        ("18", "3", "24c2e06f71ae553a408caa3f722254db2cbf1ca4db274542302184e3d6ca7015"),
        ("18", "4", "51de613e8fda20cc92979265cf7179288df8c1af4202f02794ad7327fda2657b"),
        ("18", "5", "c70354bfa312603e4819efce11a242ddcc3830895453d9424f0c83f7ae98bc5b"),
        ("18", "6", "3450433a8697b27e43172043be68d31515a7c7c00b2b248f84043dd70a2f59a8"),
        ("18", "7", "10ba41422b7a3eb5b32bc6453231100544cf620c764ab8332c629a3b9fc749d4"),
        ("18", "8", "73968dc0fd99bcbd5eae2223bd54f414879c062ac933948ba6b8b67383dc6a53"),
        ("18", "9", "e7d72fa31560f1e8ea572b8c73259d9fe512f56fbeb1b58ae014c43b9b5b6290"),
        ("18", "10", "1bee419a3b0b686a729aa12515b0f96a9a8f43478ca2c01ea1661cc1698c6266"),
        ("18", "11", "926557f0c137ea8dbf99a0487b25e131b12dfd39977d3e515f01f49187e6a09c"),
        ("18", "12", "7e2645d539d257f7064808308048622818c9083dedfa4ac0a958cd15181231ac"),
        ("18", "13", "95d2e33d0d05b8f9b6d8091d1c804271ec3a69e9aef792cc3b1ab8a2165eca3e"),
        ("18", "14", "a1adfb072f60ffcb67adb589df7c5578629441bee4ccb89ab635a6e8d7a35277"),
        ("18", "15", "4deb3df329c05729561dcc7310e49059eaddc504c4210ad31fad11dc70f61742"),
        ("18", "16", "cf02f9b949127363bad1aa700ab662a3c7cf9ce0e2e4750e066d2204b9500a99"),
        ("18", "17", "480300f949e0dd6402051810a9714adb388cf96e454a55346c76954cdd69413d"),
        ("16", "1.txt", "c7ef2303bb35131a48e2256c5a3c7b391efa73e2acf757d7e39760efb6320ed4"),
        ("16", "2", "a4db183f7c337a67f5d6b5015e3ae0af0d0edaa56894f0e9e3469c99708fed1c"),
        ("16", "3", "5b279531c42445c6f58281dd94588460218d2258ec9013c8447f3e2b7b81bf02"),
        ("16", "4", "035bddd63bc9d5fd6de26beab31887e5c14c3caa4958d2424d72f3c49832bd42"),
        ("16", "5", "02d8a1fcb6baa466de4e3683afa48076394acd805f490fbbe50ab19040675136"),
        ("16", "6", "69a3e64d75255d9179c98a2b3a63fe76d5be08c9fc41f27ac197663c97915113"),
        ("16", "7", "0d674c907758e90a168345e6b35b7a0de79c2ead390ab372465a354fcab67d17"),
        ("16", "8", "d722c0db46af905a5bd13b60e3130c4ddfb0c9da86df0a33253e5f8d53068946"),
        ("16", "9", "b563e744fbc50c1240d23df369750879df2cec69fba933704b97a73a66d9c4f1"),
        ("16", "10", "99affc65740080b7a1ab87c5c9119bf5be7cf47b2b2d8fc13407d35bd2ba6238"),
        ("16", "11", "86b89dbcae80ef48720fd3c7da88cffbdabfd4021af5a827339b56a33ddae27a"),
        ("16", "12", "c8d61d1efbd44086f88d74ad9e07dfdc3737dc7053c7d2503131ba0918973a03"),
        ("16", "13", "5ce28e6e0118a4780ad72fc096e617c874cde7d140e15f87451babb25aaf2d8f"),
        ("16", "14", "93703e734e76da30a5e050189a66d5a4d6bec5885752503c4c798e2f44049080"),
        ("16", "15", "a156ec246cd06688043cefde24de0d715fd46b08f5c0235015c2c5c3c6e37488"),
    ]
    for ver, num, checksum in patches:
        patch_url_str = "https://ambermd.org/bugfixes/{0}.0/update.{1}"
        patch(patch_url_str.format(ver, num), sha256=checksum, level=0, when="@{0}".format(ver))

    # Patch to move the namelist sebomd after the variable declarations
    # Taken from http://archive.ambermd.org/202105/0098.html
    patch("sebomd_fix.patch", when="@20")

    # Patch to add ppc64le in config.guess
    patch("ppc64le.patch", when="@18: target=ppc64le:")

    # Patch to add aarch64 in config.guess
    patch("aarch64.patch", when="@18: target=aarch64:")

    # Workaround to modify the AmberTools script when using the NVIDIA
    # compilers
    patch("nvhpc.patch", when="@18: %nvhpc")

    # Workaround to use NVIDIA compilers to build the bundled Boost
    patch("nvhpc-boost.patch", when="@18: %nvhpc")

    variant("mpi", description="Build MPI executables", default=True)
    # (Note: Set NCCL_HOME to your NCCL install path.)
    variant("nccl", description="Use NCCL for inter-GPU communications", default=False)
    variant("mkl", description="Use Intel MKL for BLAS/LAPACK routines, as well as FFTW if no other FFTW specified; incompatible with the GOTO and -macAccelerate options", default=False)
    variant("openmp", description="Use OpenMP pragmas to parallelize", default=False)
    variant("x11", description="Build programs that provide GUI (require X11)", default=False)
    variant("update", description="Update the sources prior compilation", default=False)
    variant("plumed", description="plumed", default=False)
    variant("perl", description="build perl components (FEW and mm_pbsa) ", default=False)
    variant("quick", description="build  QUICK ab initio QM code and ab initio QM/MM capability in SANDER", default=False)
    variant("tests", description="install tests ( larger install size)", default=False)
    variant("python", description="use python packages", default=False)

    depends_on("zlib-api")
    depends_on("readline")
    depends_on("libx11", type=("run", "link"), when="+x11")
    depends_on("python+tkinter", when="+python")
    depends_on("perl", when="+perl", type=("run", "link"))
    depends_on("perl", type=("build"))
    depends_on("py-numpy", when="+python")
    depends_on("py-mpi4py", when="+python+mpi")
    depends_on("py-scipy", when="+python")
    depends_on("py-matplotlib", when="+python")
    depends_on("py-setuptools", when="+python")
    depends_on("fftw", when="~mkl")
    depends_on("plumed+mpi", when="+mpi")
    depends_on("plumed~mpi", when="~mpi")

    depends_on("bzip2")
    depends_on("flex", type="build")
    depends_on("bison", type="build")
    depends_on("netcdf-fortran")
    depends_on("netcdf-c")
    depends_on("parallel-netcdf", when="@20:")  # when='AmberTools@21:'
    depends_on("arpack-ng")
    depends_on("protobuf")
    depends_on("boost+chrono+filesystem+graph+iostreams+program_options+regex+system+thread+timer")
    depends_on("netlib-xblas")
    depends_on("tcsh", type=("build"), when="@20")  # when='AmberTools@21:'
    # Potential issues with openmpi 4
    # (http://archive.ambermd.org/201908/0105.html)
    depends_on("mpi", when="+mpi")

    # Cuda dependencies
    # /AmberTools/src/configure2:1329
    #depends_on("cuda@:11.1", when="@20:+cuda")  # when='AmberTools@21:'
    depends_on("cuda", when="@20:+cuda")  # when='AmberTools@21:'
    depends_on("cuda@:10.2.89", when="@18+cuda")
    depends_on("cuda@7.5.18", when="@:16+cuda")
    depends_on("nccl", when="+nccl")
    depends_on("intel-oneapi-mkl", when="+mkl")

    # conflicts
    conflicts("+x11", when="platform=cray", msg="x11 amber applications not available for cray")
    conflicts("+openmp", when="%clang", msg="OpenMP not available for the clang compiler")
    conflicts(
        "+openmp", when="%apple-clang", msg="OpenMP not available for the Apple clang compiler"
    )
    conflicts("+openmp", when="%pgi", msg="OpenMP not available for the pgi compiler")

    def url_for_version(self, version):
        url = "file://{0}/Amber{1}.tar.bz2".format(os.getcwd(), version)
        return url

    def patch(self):
        # this funcions try to move, merging folders, in case there is a collision, does not copy and issue a warning
        def my_copy(from_path,to_path):
            if os.path.exists(to_path):
                if os.path.isdir(to_path):
                    for p in os.listdir(from_path):
                        my_copy(join_path(from_path,p),join_path(to_path,p))
                else:
                    tty.warn("Path " + to_path + " already present, skip move of " + from_path)
            else:
                os.rename(from_path,to_path)

        my_copy(join_path(self.stage.source_path, "ambertools_tmpdir"),self.stage.source_path)

        # CudaConfig seem too much picky about compatibility between gcc and cuda versions, extending compatibility from cuda 11.6 to 11.8
        filter_file(
                r'CUDA_VERSION VERSION_LESS_EQUAL 11.6',
                'CUDA_VERSION VERSION_LESS_EQUAL 11.8',
                join_path(self.stage.source_path, "cmake", "CudaConfig.cmake"),
                string=True,
                )
        filter_file(
                r'VERSION_LESS_EQUAL 11.6',
                'VERSION_LESS_EQUAL 11.8',
                join_path(self.stage.source_path, "AmberTools", "src", "quick", "quick-cmake", "QUICKCudaConfig.cmake"),
                string=True,
                )
        filter_file(
                r'fftw_mpi_init FFTW_MPI_WORKS',
                'fftw_mpi_init FFTW_MPI_WORKS ${MPI_mpi_LIBRARY}',
                join_path(self.stage.source_path, "cmake", "jedbrown", "FindFFTW.cmake"),
                string=True,
                )
        filter_file(
                r'LIBRARIES ${PLUMED_LIBRARIES}',
                'LIBRARIES ${PLUMED_LIBRARIES} ${MPI_mpi_LIBRARY}',
                join_path(self.stage.source_path, "cmake", "FindPLUMED.cmake"),
                string=True,
                )


        
        
    def setup_build_environment(self, env):

        # UPDATES
        if self.spec.satisfies("+update"):
            amber_src = self.stage.source_path
            env.set("AMBERSOURCE", amber_src)
            env.set("AMBERHOME", amber_src)
            env.set("AMBER_SOURCE", amber_src)

        if self.spec.satisfies("+plumed"):
            env.set("PLUMED_ROOT", self.spec["plumed"].prefix)

        # The bundled Boost does not detect the bzip2 package, but
        # will silently fall back to a system install (if available).
        # Force it to use the bzip2 package.
        env.prepend_path("CPATH", self.spec["bzip2"].prefix.include)

        # CUDA
        if self.spec.satisfies("+cuda"):
            env.set("CUDA_HOME", self.spec["cuda"].prefix)

        # NCCL
        if self.spec.satisfies("+nccl"):
            env.set("NCCL_HOME", self.spec["nccl"].prefix)

        # MPI
        if self.spec.satisfies("+mpi"):
            env.set("MPI_HOME", self.spec["mpi"].prefix)



    def cmake_args(self):

        # The resource command does not allow us to expand the package in the
        # root stage folder as required, as it already contains files. Here we
        # install AmberTools where it should be, which results in 3 copies of
        # the  ambertools (~9 GB). This has to be improved in the future.
        #shutil_copytree.copytree(join_path(self.stage.source_path, "ambertools_tmpdir"), self.stage.source_path, dirs_exist_ok=True)
        # I cannot remove the folder, because apparently copytree is asynchronous
        #shutil.rmtree(join_path(self.stage.source_path, "ambertools_tmpdir"))

        spec = self.spec

        netcdfIncf=join_path(self.spec["netcdf-fortran"].prefix, "include")
        netcdfLibf=join_path(self.spec["netcdf-fortran"].prefix, "lib")
        netcdflsof=join_path(netcdfLibf, "libnetcdff.so")
        netcdfIncc=join_path(self.spec["netcdf-c"].prefix, "include")
        netcdfLibc=join_path(self.spec["netcdf-c"].prefix, "lib")
        netcdflsoc=join_path(netcdfLibc, "libnetcdf.so")
        amber_src = self.stage.source_path
        ambertoolsPath=join_path(amber_src, "AmberTools")
        ambertoolsSrc=join_path(ambertoolsPath, "src")
        # Select compiler style
        if self.spec.satisfies("%cce"):
            compiler = "cray"
        elif self.spec.satisfies("%gcc"):
            compiler = "gnu"
        elif self.spec.satisfies("%intel"):
            compiler = "intel"
        elif self.spec.satisfies("%pgi"):
            compiler = "pgi"
        elif self.spec.satisfies("%nvhpc"):
            compiler = "pgi"
        elif self.spec.satisfies("%clang"):
            compiler = "clang"
        else:
            raise InstallError("Unknown compiler, exiting!!!")

        base_cmakeargs = ["-DDOWNLOAD_MINICONDA:BOOL=OFF",
        "-DTRUST_SYSTEM_LIBS=TRUE",
        "-DnetCDF_C_LIBRARY="+netcdflsoc,
        "-DnetCDF_C_INCLUDE_DIR="+netcdfLibc,
        "-DNetCDF_LIBRARIES_C="+netcdflsoc,
        "-DNetCDF_INCLUDES="+netcdfIncc,
        "-DNetCDF_LIBRARIES_F77="+netcdflsof,
        "-DNetCDF_LIBRARIES_F90="+netcdflsof,
        "-DNetCDF_INCLUDES_F77="+netcdfIncf,
        "-DNetCDF_INCLUDES_F90="+netcdfIncf,
        "-DCOMPILER="+compiler.upper(),
        ]
        if self.spec.satisfies("+mkl"):
            base_cmakeargs.append(
                "-DMKL_HOME="+self.spec["mkl"].prefix,
            )
        base_cmakeargs.append("-DBOOST_ROOT={0}".format(spec["boost"].prefix))
        if self.spec.satisfies("+plumed"):
            base_cmakeargs.append("-DPLUMED_ROOT={0}".format(spec["plumed"].prefix))
#            base_cmakeargs.append("-DPLUMED_DIR={0}".format(spec["plumed"].prefix.include))
#            base_cmakeargs.append("-DPLUMED_LIBRARY={0}".format(spec["plumed"].prefix.lib))
        base_cmakeargs.append(self.define("MPI_HOME", spec["mpi"].prefix))

        # patching python
#luigi        if self.spec.satisfies("+python"):
#luigi            pythonBin=join_path(self.spec["python"].prefix, "bin")
#luigi            pythonExe=join_path(pythonBin, "python")
#luigi            pytrjPath=join_path(ambertoolsSrc, "pytraj")
#luigi            pytrjcmake=join_path(pytrjPath, "CMakeLists.txt")
#luigi            base_cmakeargs.append("-DPYTHON_EXECUTABLE:FILEPATH="+pythonExe)
#luigi            filter_file(
#luigi                r'	COMMAND ${CMAKE_COMMAND} -E touch ${STAMP_FILE}',
#luigi                '	COMMAND ${CMAKE_COMMAND} -E make_directory ${BUILD_DIR}\n	COMMAND ${CMAKE_COMMAND} -E touch ${STAMP_FILE}',
#luigi                pytrjcmake,
#luigi                string=True,
#luigi                )
        cmake_args = base_cmakeargs

        variant_option_exceptions = {"python": "BUILD_PYTHON",
                                     "perl": "BUILD_PERL",
                                     "quick": "BUILD_QUICK",
                                     "x11": "BUILD_GUI",
                                     "tests": "INSTALL_TESTS",
                                     "update": "CHECK_UPDATES",
                                    }
        variant_options = ["openmp", "cuda", "nccl", "mpi", "python", "perl", "quick", "x11", "tests", "update"]

        for variant in variant_options:
            cmake_args.append(
                self.define_from_variant(variant_option_exceptions.get(variant,variant.upper()), variant)
            )

#luigi        if self.spec.satisfies("+openmp"):
#luigi            cmake_args.append(
#luigi                self.define_from_variant("OPENMP", "openmp"),
#luigi            )

#luigi        if self.spec.satisfies("+cuda"):
#luigi            cmake_args.append(
#luigi                self.define_from_variant("CUDA", "cuda"),
#luigi            )

#luigi        if  self.spec.satisfies("+nccl"):
#luigi            cmake_args.append(
#luigi                self.define_from_variant("NCCL", "nccl"),
#luigi            )

#luigi        if self.spec.satisfies("+mpi"):
#luigi            cmake_args.append(
#luigi                self.define_from_variant("MPI", "mpi"),
#luigi            )

            ## in case prefers taking MPI compiler wrappers as CMake compilers, comment out these lines.
            #if "+mpi" in spec:
            #    cmake_args.append(self.define("CMAKE_C_COMPILER", spec["mpi"].mpicc))
            #    cmake_args.append(self.define("CMAKE_Fortran_COMPILER", spec["mpi"].mpifc))
        return cmake_args




    def setup_run_environment(self, env):
        env.set("AMBER_PREFIX", self.prefix)
        env.set("AMBERHOME", self.prefix)
        # CUDA
        if self.spec.satisfies("+cuda"):
            env.prepend_path("LD_LIBRARY_PATH", self.spec["cuda"].prefix.lib)


