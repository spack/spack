# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform
import re  # To get the variant name after (+)

import spack.build_systems.cmake
import spack.build_systems.makefile
from spack.package import *


def find_model_flag(str):
    res = re.findall(r"\+(\w+)", str)
    if not res:
        return ""
    return res


def find_package_version(s):
    try:
        start = s.index("-", s.index("-", s.index("-") + len("-")))
        end = s.index("-", start)
        return s[start:end]
    except ValueError:
        return ""


class Babelstream(CMakePackage, CudaPackage, ROCmPackage, MakefilePackage):
    """Measure memory transfer rates to/from global device memory on GPUs.
    This benchmark is similar in spirit, and based on, the STREAM benchmark for CPUs."""

    homepage = "https://github.com/UoB-HPC/BabelStream"
    url = "https://github.com/UoB-HPC/BabelStream/archive/refs/tags/v4.0.tar.gz"
    git = "https://github.com/UoB-HPC/BabelStream.git"
    version("4.0", sha256="a9cd39277fb15d977d468435eb9b894f79f468233f0131509aa540ffda4f5953")
    version("main", branch="main")
    version("develop", branch="develop")

    maintainers("tomdeakin", "kaanolgu", "tom91136", "robj0nes")
    build_system("cmake", "makefile", default="cmake")
    # Languages
    # Also supported variants are cuda and rocm (for HIP)
    variant("sycl", default=False, description="Enable SYCL support")
    variant("sycl2020", default=False, description="Enable SYCL support")
    variant("omp", default=False, description="Enable OpenMP support")
    variant("ocl", default=False, description="Enable OpenCL support")
    variant("tbb", default=False, description="Enable TBB support")
    variant("acc", default=False, description="Enable OpenACC support")
    variant("thrust", default=False, description="Enable THRUST support")
    variant("raja", default=False, description="Enable RAJA support")
    variant("stddata", default=False, description="Enable STD-data support")
    variant("stdindices", default=False, description="Enable STD-indices support")
    variant("stdranges", default=False, description="Enable STD-ranges support")

    # Some models need to have the programming model abstraction downloaded -
    # this variant enables a path to be provided.
    variant("dir", values=str, default="none", description="Enable Directory support")

    # Kokkos conflict and variant
    conflicts(
        "dir=none", when="+kokkos", msg="KOKKKOS requires architecture to be specfied by dir="
    )
    variant("kokkos", default=False, description="Enable KOKKOS support")

    # ACC conflict
    variant("cpu_arch", values=str, default="none", description="Enable CPU Target for ACC")
    variant("target", values=str, default="none", description="Enable CPU Target for ACC")

    # STD conflicts
    conflicts("+stddata", when="%gcc@:10.1.0", msg="STD-data requires newer version of GCC")
    conflicts("+stdindices", when="%gcc@:10.1.0", msg="STD-indices requires newer version of GCC")
    conflicts("+stdranges", when="%gcc@:10.1.0", msg="STD-ranges requires newer version of GCC")

    # CUDA conflict
    conflicts(
        "cuda_arch=none",
        when="+cuda",
        msg="CUDA requires architecture to be specfied by cuda_arch=",
    )
    variant("mem", values=str, default="DEFAULT", description="Enable MEM Target for CUDA")
    # Raja Conflict
    variant(
        "offload",
        values=str,
        default="none",
        description="Enable RAJA Target [CPU or NVIDIA] / Offload with custom settings for OpenMP",
    )
    conflicts(
        "offload=none",
        when="+raja",
        msg="RAJA requires architecture to be specfied by target=[CPU,NVIDIA]",
    )

    # download raja from https://github.com/LLNL/RAJA
    conflicts(
        "dir=none",
        when="+raja",
        msg="RAJA implementation requires architecture to be specfied by dir=",
    )

    # Thrust Conflict
    # conflicts("~cuda", when="+thrust", msg="Thrust requires +cuda variant")
    depends_on("thrust", when="+thrust")
    depends_on("rocthrust", when="+thrust implementation=rocm")

    # TBB Dependency
    depends_on("intel-oneapi-tbb", when="+tbb")
    partitioner_vals = ["auto", "affinity", "static", "simple"]
    variant(
        "partitioner",
        values=partitioner_vals,
        default="auto",
        description="Partitioner specifies how a loop template should partition its work among threads.\
            Possible values are:\
            AUTO     - Optimize range subdivision based on work-stealing events.\
            AFFINITY - Proportional splitting that optimizes for cache affinity.\
            STATIC   - Distribute work uniformly with no additional load balancing.\
            SIMPLE   - Recursively split its range until it cannot be further subdivided.\
            See https://spec.oneapi.com/versions/latest/elements/oneTBB/source/algorithms.html#partitioners for more details.",
    )
    # OpenMP Intel Offload
    variant("intel_target", values=str, default="none", description="Intel Offload target")
    # Kokkos Dependency
    depends_on("kokkos@3.7.1", when="+kokkos")

    # OpenCL Dependency

    backends = {
        "ocl": [
            ("amd", "rocm-opencl", "enable ROCM backend"),
            ("cuda", "cuda", "enable Cuda backend"),
            ("intel", "intel-oneapi-compilers", "enable Intel backend"),
            ("pocl", "pocl@1.5", "enable POCL backend"),
        ],
        "kokkos": [
            ("cuda", "cuda", "enable Cuda backend"),
            ("omp", "none", "enable Cuda backend"),
        ],
    }
    backend_vals = ["none"]
    for lang in backends:
        for item in backends[lang]:
            backend, dpdncy, descr = item
            backend_vals.append(backend.lower())

    variant("backend", values=backend_vals, default="none", description="Enable backend support")

    for lang in backends:
        for item in backends[lang]:
            backend, dpdncy, descr = item
            if dpdncy.lower() != "none":
                depends_on("%s" % dpdncy.lower(), when="backend=%s" % backend.lower())
    # this flag could be used in all required languages
    variant("flags", values=str, default="none", description="Additional CXX flags to be provided")

    # comp_impl_vals=["ONEAPI-DPCPP","DPCPP","HIPSYCL","COMPUTECPP"]
    with when("build_system=cmake"):
        variant(
            "implementation",
            values=str,
            default="none",
            description="Compile using the specified SYCL compiler option",
        )
        conflicts(
            "implementation=none",
            when="+sycl",
            msg="SYCL requires compiler implementation to be specified by option=",
        )
        conflicts(
            "implementation=none",
            when="+thrust",
            msg="Which Thrust implementation to use, supported options include:\
            - CUDA (via https://github.com/NVIDIA/thrust)\
            - ROCM (via https://github.com/ROCmSoftwarePlatform/rocThrust)",
        )

    # This applies to all
    depends_on("cmake@3.14.0:", type="build")
    depends_on("opencl-c-headers", when="+ocl")
    implementation_vals_cmake = ["cuda", "rocm", "oneapi-dpcpp", "dpcpp", "hipsycl", "computecpp"]

    with when("build_system=makefile"):
        implementation_vals = [
            "DoConcurrent",
            "Array",
            "OpenMP",
            "OpenMPWorkshare",
            "OpenMPTarget",
            "OpenMPTargetLoop",
            "OpenMPTaskloop",
            "OpenACC",
            "OpenACCArray",
            "CUDA",
            "CUDAKernel",
            "Sequential",
        ]
        variant(
            "impl", values=implementation_vals, default="Sequential", description="Implementation"
        )
        # The fortran Makefile is inside the src/fortran so we need to address this
        build_directory = "src/fortran"
        # build_directory = '.'
        build_name = ""

        variant(
            "test", values=str, default="none", description="Test Variant for debugging purposes"
        )


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        # convert spec to string to work on it
        spec_string = str(self.spec)

        # take only the first portion of the spec until space
        spec_string_truncate = spec_string.split(" ", 1)[0]
        model_list = find_model_flag(spec_string_truncate)  # Prints out ['cuda', 'thrust']

        if len(model_list) > 1:
            ignore_list = ["cuda"]  # if +acc is provided ignore the cuda model
            model = list(set(model_list) - set(ignore_list))
            # We choose 'thrust' from the list of ['cuda', 'thrust']
            args = ["-DMODEL=" + model[0]]
        else:
            # if it is +stddata,indices etc. we need to pass it
            # as std-data to the CMake compiler
            # do some alterations here
            if "std" in model_list[0]:
                args = ["-DMODEL=" + "std-" + model_list[0].split("d", 1)[1]]
            else:
                args = ["-DMODEL=" + model_list[0]]

        # ===================================
        #             ACC
        # ===================================
        if ("+acc" in self.spec) and ("~cuda" in self.spec):
            args.append("-DCMAKE_CXX_COMPILER=" + self.compiler.cxx)
            if "cuda_arch" in self.spec.variants:
                cuda_arch_list = self.spec.variants["cuda_arch"].value
                # the architecture value is only number so append sm_ to the name
                cuda_arch = "cc" + cuda_arch_list[0]
                args.append("-DTARGET_DEVICE=gpu")
                args.append("-DCUDA_ARCH=" + cuda_arch)
            elif "cpu_arch" in self.spec.variants:
                cpu_arch_list = self.spec.variants["cpu_arch"].value
                # the architecture value is only number so append sm_ to the name
                # cpu_arch = cpu_arch_list[0]
                args.append("-DTARGET_DEVICE=multicore")
                args.append("-DTARGET_PROCESSOR=" + cpu_arch_list)

        # ===================================
        #    STDdata,STDindices,STDranges
        # ===================================
        std_list = ["+stddata", "+stdindices", "+stdranges"]
        if spec_string.startswith(tuple(std_list)):
            args.append("-DCMAKE_CXX_COMPILER=" + self.compiler.cxx)
            if "offload" in self.spec.variants:
                cuda_arch_list = self.spec.variants["offload"].value
                # the architecture value is only number so append sm_ to the name
                cuda_arch = "cc" + cuda_arch_list[0]
                args.append("-DNVHPC_OFFLOAD=" + cuda_arch)
                # cuda_dir = self.spec["cuda"].prefix
                # cuda_comp = cuda_dir + "/bin/nvcc"
                # args.append("-DCMAKE_CUDA_COMPILER=" + cuda_comp)
        # ===================================
        #             CUDA
        # ===================================

        if ("+cuda" in self.spec) and ("~kokkos" in self.spec) and ("~acc" in self.spec):
            # Set up the cuda macros needed by the build
            cuda_arch_list = self.spec.variants["cuda_arch"].value
            # the architecture value is only number so append sm_ to the name
            cuda_arch = "sm_" + cuda_arch_list[0]
            args.append("-DCUDA_ARCH=" + cuda_arch)
            cuda_dir = self.spec["cuda"].prefix
            cuda_comp = cuda_dir + "/bin/nvcc"
            args.append("-DCMAKE_CUDA_COMPILER=" + cuda_comp)
            args.append("-DMEM=" + self.spec.variants["mem"].value)
            if self.spec.variants["flags"].value != "none":
                args.append("-DCUDA_EXTRA_FLAGS=" + self.spec.variants["flags"].value)

        # ===================================
        #             OMP
        # ===================================
        # `~kokkos` option is there to prevent +kokkos +omp setting to use omp directly from here
        # Same applies for raja
        if ("+omp" in self.spec) and ("~kokkos" in self.spec) and ("~raja" in self.spec):
            args.append("-DCMAKE_CXX_COMPILER=" + self.compiler.cxx)
            if "cuda_arch" in self.spec.variants:
                cuda_arch_list = self.spec.variants["cuda_arch"].value
                # the architecture value is only number so append sm_ to the name
                cuda_arch = "sm_" + cuda_arch_list[0]
                args.append("-DOFFLOAD= " + "NVIDIA:" + cuda_arch)
            elif "amdgpu_target" in self.spec.variants:
                rocm_arch = self.spec.variants["amdgpu_target"].value
                # the architecture value is only number so append sm_ to the name
                args.append("-DOFFLOAD=" + " AMD:" + rocm_arch)
            elif ("intel_target" in self.spec.variants) and (
                self.spec.variants["intel_target"].value != "none"
            ):
                args.append("-DOFFLOAD=" + "INTEL")
            elif "offload" in self.spec.variants and (
                self.spec.variants["offload"].value != "none"
            ):
                args.append("-DOFFLOAD=" + "ON")
                args.append("-DOFFLOAD_FLAGS=" + self.spec.variants["offload"].value)
            else:
                args.append("-DOFFLOAD=" + "OFF")

        # ===================================
        #             SYCL
        # ===================================

        if "+sycl" in self.spec:
            args.append("-DSYCL_COMPILER=" + self.spec.variants["implementation"].value.upper())
            if self.spec.variants["implementation"].value.upper() != "ONEAPI-DPCPP":
                args.append(
                    "-DSYCL_COMPILER_DIR=" + self.spec.variants["implementation"].value.upper()
                )
                if self.spec.variants["implementation"].value.upper() == "COMPUTE-CPP":
                    args.append("-DOpenCL_LIBRARY=")

        # ===================================
        #             SYCL 2020
        # ===================================

        if "+sycl2020" in self.spec:
            if self.spec.satisfies("%oneapi"):
                # -fsycl flag is required for setting up sycl/sycl.hpp seems like
                #  it doesn't get it from the CMake file
                args.append("-DCXX_EXTRA_FLAGS= -fsycl -O3")
                # this is required to enable -DCMAKE_CXX_COMPILER=icpx flag from CMake
                args.append("-DSYCL_COMPILER=ONEAPI-ICPX")
            else:
                args.append(
                    "-DSYCL_COMPILER=" + self.spec.variants["implementation"].value.upper()
                )
                if self.spec.variants["implementation"].value.upper() != "ONEAPI-DPCPP":
                    args.append(
                        "-DSYCL_COMPILER_DIR=" + self.spec.variants["implementation"].value.upper()
                    )
                    if self.spec.variants["implementation"].value.upper() == "COMPUTE-CPP":
                        args.append("-DOpenCL_LIBRARY=")

        # ===================================
        #             HIP(ROCM)
        # ===================================

        if "+rocm" in self.spec:
            hip_comp = self.spec["rocm"].prefix + "/bin/hipcc"
            args.append("-DCMAKE_CXX_COMPILER=" + hip_comp)
            args.append(
                "-DCXX_EXTRA_FLAGS= --offload-arch="
                + self.spec.variants["amdgpu_target"].value
                + " "
                + self.spec.variants["flags"].value
                + " -O3"
            )

        # ===================================
        #             TBB
        # ===================================

        if "+tbb" in self.spec:
            args.append("-DONE_TBB_DIR=" + self.spec["tbb"].prefix + "/tbb/latest/")
            args.append("-DPARTITIONER=" + self.spec.variants["partitioner"].value.upper())

        # ===================================
        #             OpenCL (ocl)
        # ===================================
        if "+ocl" in self.spec:
            if "backend" in self.spec.variants:
                if "cuda" in self.spec.variants["backend"].value:
                    cuda_dir = self.spec["cuda"].prefix
                    args.append("-DOpenCL_LIBRARY=" + cuda_dir + "/lib64/libOpenCL.so")
                elif "amd" in self.spec.variants["backend"].value:
                    rocm_dir = self.spec["rocm-opencl"].prefix
                    args.append("-DOpenCL_LIBRARY=" + rocm_dir + "/lib64/libOpenCL.so")
                elif "intel" in self.spec.variants["backend"].value:
                    # extracting the inter compiler package version
                    path_to_intel_compiler = os.path.basename(
                        self.spec["intel-oneapi-compilers"].prefix
                    )
                    comp_version = find_package_version(path_to_intel_compiler)
                    intel_lib = (
                        self.spec["intel-oneapi-compilers"].prefix
                        + "/compiler/"
                        + comp_version
                        + "/linux/lib/libOpenCL.so"
                    )
                    args.append("-DOpenCL_LIBRARY=" + intel_lib)
                elif "pocl" in self.spec.variants["backend"].value:
                    args.append("-DCMAKE_CXX_COMPILER=" + self.compiler.cxx)
                    pocl_lib = self.spec["pocl"].prefix + "/lib64/libOpenCL.so"
                    args.append("-DOpenCL_LIBRARY=" + pocl_lib)
                args.append("-DCMAKE_CXX_COMPILER=" + self.compiler.cxx)

        # ===================================
        #             RAJA
        # ===================================
        if "+raja" in self.spec:
            args.append("-DCMAKE_CXX_COMPILER=" + self.compiler.cxx)
            args.append("-DRAJA_IN_TREE=" + self.spec.variants["dir"].value)
            if "offload" in self.spec.variants:
                if "nvidia" in self.spec.variants["offload"].value:
                    cuda_dir = self.spec["cuda"].prefix
                    cuda_comp = cuda_dir + "/bin/nvcc"
                    args.append("-DCMAKE_CUDA_COMPILER=" + cuda_comp)
                    args.append("-DTARGET=NVIDIA")
                    cuda_arch_list = self.spec.variants["cuda_arch"].value
                    int_cuda_arch = int(cuda_arch_list[0])
                    cuda_arch = "sm_" + cuda_arch_list[0]
                    args.append("-DCUDA_ARCH=" + cuda_arch)

                    args.append("DCUDA_TOOLKIT_ROOT_DIR=" + self.spec["cuda"].prefix)
                    if self.spec.variants["flags"].value != "none":
                        args.append("-DCUDA_EXTRA_FLAGS=" + self.spec.variants["flags"].value)
                # if("cpu" in self.spec.variants['offload'].value):

            if "omp" in self.spec.variants["backend"].value:
                args.append("-DENABLE_OPENMP=ON")
            if "cuda" in self.spec.variants["backend"].value:
                args.append("-DENABLE_CUDA=ON")

        # ===================================
        #             THRUST
        # ===================================
        if "+thrust" in self.spec:
            if "cuda" in self.spec.variants["implementation"].value:
                args.append("-DTHRUST_IMPL=" + self.spec.variants["implementation"].value.upper())
                args.append("-SDK_DIR=" + self.spec["thrust"].prefix + "/include")
                cuda_arch_list = self.spec.variants["cuda_arch"].value
                # the architecture value is only number so append sm_ to the name
                cuda_arch = "sm_" + cuda_arch_list[0]
                args.append("-DCUDA_ARCH=" + cuda_arch)
                cuda_dir = self.spec["cuda"].prefix
                cuda_comp = cuda_dir + "/bin/nvcc"
                args.append("-DCMAKE_CUDA_COMPILER=" + cuda_comp)
                args.append("-DBACKEND=" + self.spec.variants["backend"].value.upper())
                if self.spec.variants["flags"].value != "none":
                    args.append("-DCUDA_EXTRA_FLAGS=" + self.spec.variants["flags"].value)

            if "rocm" in self.spec.variants["implementation"].value:
                args.append("-DTHRUST_IMPL=" + self.spec.variants["implementation"].value.upper())
                args.append("-SDK_DIR=" + self.spec["rocthrust"].prefix)
                args.append("-DBACKEND=" + self.spec.variants["backend"].value.upper())

        # ===================================
        #             kokkos
        # ===================================
        # kokkos implementation is versatile and it could use cuda or omp architectures as backend
        # The usage should be spack install babelstream +kokkos +cuda [or +omp]
        if "+kokkos" in self.spec:
            args.append("-DCMAKE_CXX_COMPILER=" + self.compiler.cxx)
            args.append("-DKOKKOS_IN_TREE=" + self.spec.variants["dir"].value)
            # args.append("-DKOKKOS_IN_PACKAGE=" + self.spec["kokkos"].prefix)
            if "backend" in self.spec.variants:
                if "cuda" in self.spec.variants["backend"].value:
                    args.append("-DKokkos_ENABLE_CUDA=ON")
                    cuda_arch_list = self.spec.variants["cuda_arch"].value
                    int_cuda_arch = int(cuda_arch_list[0])
                    # arhitecture kepler optimisations
                    if int_cuda_arch in (30, 32, 35, 37):
                        args.append("-D" + "Kokkos_ARCH_KEPLER" + str(int_cuda_arch) + "=ON")
                    # arhitecture maxwell optimisations
                    if int_cuda_arch in (50, 52, 53):
                        args.append("-D" + "Kokkos_ARCH_MAXWELL" + str(int_cuda_arch) + "=ON")
                    # arhitecture pascal optimisations
                    if int_cuda_arch in (60, 61):
                        args.append("-D" + "Kokkos_ARCH_PASCAL" + str(int_cuda_arch) + "=ON")
                    # architecture volta optimisations
                    if int_cuda_arch in (70, 72):
                        args.append("-D" + "Kokkos_ARCH_VOLTA" + str(int_cuda_arch) + "=ON")
                    if int_cuda_arch == 75:
                        args.append("-DKokkos_ARCH_TURING75=ON")
                if "omp" in self.spec.variants["backend"].value:
                    args.append("-DKokkos_ENABLE_OPENMP=ON")

        # not in ["kokkos", "raja", "acc", "hip"] then compiler forced true
        if set(model_list).intersection(["kokkos", "raja", "acc", "hip"]) is True:
            args.append("-DCMAKE_CXX_COMPILER_FORCED=True")

        return args


class MakefileBuilder(spack.build_systems.makefile.MakefileBuilder):
    build_directory = "src/fortran"

    # Generate Compiler Specific includes
    def edit(self, pkg, spec, prefix):
        config = {
            "FC": pkg.compiler.fc_names[0],
            "FCFLAGS": "",
            "ARCH": platform.machine(),
            "DOCONCURRENT_FLAG": "",
            "ARRAY_FLAG": "",
            "OPENMP_FLAG": "",
            "OPENACC_FLAG": "",
            "CUDA_FLAG": "",
            "SEQUENTIAL_FLAG": "",
        }

        # ===================================
        #               ARM
        # ===================================
        if spec.compiler.name == "arm":
            flags = "-std=f2018 " + pkg.compiler.opt_flags[4] + " -Wall -Wno-unused-variable"

            if platform.machine() == "aarch64":
                # TODO: Add MCPU option here as in -mcpu=$(MCPU)
                flags += "-mcpu=native"
            else:
                # TODO: Add MARCH option here as in -march=$(MARCH)
                flags += "-march=native"

            config["DOCONCURRENT_FLAG"] = pkg.compiler.openmp_flag  # libomp.so required
            config["ARRAY_FLAG"] = pkg.compiler.openmp_flag  # libomp.so required
            config["OPENMP_FLAG"] = pkg.compiler.openmp_flag  # libomp.so required
            config["OPENACC_FLAG"] = "-fopenacc"

            # Error Messages
            if self.spec.variants["impl"].value in [
                "CUDA",
                "CUDAKernels",
                "OpenACC",
                "OpenACCArray",
            ]:
                sys.exit(self.spec.variants["impl"].value + "is not supported by this compiler")

        # ===================================
        #               AMD
        # ===================================
        if spec.compiler.name == "aocc":
            flags = (
                "-std=f2018 "
                + pkg.compiler.opt_flags[3]
                + " -Wall -Wno-unused-variable -march=native"
            )

            config["DOCONCURRENT_FLAG"] = pkg.compiler.openmp_flag  # libomp.so required
            config["ARRAY_FLAG"] = pkg.compiler.openmp_flag  # libomp.so required
            config["OPENMP_FLAG"] = pkg.compiler.openmp_flag  # libomp.so required
            config["OPENACC_FLAG"] = "-fopenacc"

            # Error Messages
            if self.spec.variants["impl"].value in ["CUDA", "CUDAKernels"]:
                sys.exit(self.spec.variants["impl"].value + "is not supported by this compiler")

        # ===================================
        #               CRAY
        # ===================================
        if spec.compiler.name == "cce":
            flags = "-e F -O3"

            config["DOCONCURRENT_FLAG"] = "-h thread_do_concurrent -DCRAY_THREAD_DOCONCURRENT"
            config["ARRAY_FLAG"] = "-h autothread"
            config[
                "OPENMP_FLAG"
            ] = pkg.compiler.openmp_flag  # if clang based it will be -fopenmp else -h omp
            config["OPENACC_FLAG"] = "-h acc"  # for cpu only -h omp

            # Error Messages
            if self.spec.variants["impl"].value in ["CUDA", "CUDAKernels"]:
                sys.exit(self.spec.variants["impl"].value + "is not supported by this compiler")

        # ===================================
        #               GCC
        # ===================================
        if spec.compiler.name == "gcc":
            flags = "-std=f2018 -O3 "
            flags += "-Wall -Wno-unused-dummy-argument -Wno-unused-variable "

            # config['MARCH'] = "neoverse-v1,neoverse-n1,icelake-server,znver3,cortex-a78ae"

            if platform.machine() == "aarch64":
                # TODO: Add MCPU option here as in -mcpu=$(MCPU)
                flags += "-mcpu=native"
            else:
                # TODO: Add MARCH option here as in -march=$(MARCH)
                flags += "-march=native"

            config["FCFLAGS"] = flags
            config["DOCONCURRENT_FLAG"] = "-ftree-parallelize-loops=4"
            config["OPENMP_FLAG"] = pkg.compiler.openmp_flag
            config["OPENACC_FLAG"] = "-fopenacc"

            # Error Messages
            if "CUDA" in self.spec.variants["impl"].value:
                sys.exit(self.spec.variants["impl"].value + "is not supported by this compiler")

        # ===================================
        #               NVHPC
        # ===================================
        if spec.compiler.name == "nvhpc":
            flags = pkg.compiler.opt_flags[4]  # for -O3
            # FCFLAGS	:= -O3 -Minform=inform -Minfo=all
            flags += " -Minform=warn "
            TARGET = "gpu"  # target = "multicore"
            config["TARGET"] = TARGET
            if "cuda_arch" in self.spec.variants:
                cuda_arch_list = self.spec.variants["cuda_arch"].value
                # the architecture value is only number so append sm_ to the name
                cuda_arch = "cc" + cuda_arch_list[0]
            # config['MARCH'] = "neoverse-v1,neoverse-n1,icelake-server,znver3,cortex-a78ae"
            GPUFLAG = " -gpu=" + cuda_arch
            # march=neoverse-v1,neoverse-n1,zen3
            march = "none"
            if march != "none":
                if platform.machine() == "aarch64":
                    if march in ["neoverse-n1", "neoverse-v1"]:
                        flags += "-tp=" + march
                    else:
                        flags += "-tp=native"
                    # TODO: Add MCPU option here as in -mcpu=$(MCPU)
                else:
                    # TODO: Add MARCH option here as in -march=$(MARCH)
                    flags += "-tp=" + march
            else:
                flags += "-tp=native"
            # this is to allow apples-to-apples comparison with DC in non-DC GPU impls
            # set exactly one of these pairs!
            # MANAGED = "-DUSE_MANAGED -gpu=managed"
            # DEVICE=""
            # ------------
            DEVICE = ("-DUSE_DEVICE -cuda -gpu=nomanaged",)
            MANAGED = ""
            config["FCFLAGS"] = flags
            config["DOCONCURRENT_FLAG"] = GPUFLAG + " -stdpar=" + TARGET + " " + DEVICE
            config["ARRAY_FLAG"] = GPUFLAG + " -stdpar=" + TARGET + " " + MANAGED
            config["OPENMP_FLAG"] = GPUFLAG + " -mp=" + TARGET + " " + MANAGED
            config["OPENACC_FLAG"] = GPUFLAG + " -acc=" + TARGET + " " + MANAGED
            config["CUDA_FLAG"] = GPUFLAG + " -cuda -acc=gpu" + " " + MANAGED

            # Error Messages
            if self.spec.variants["impl"].value in ["OpenMPTaskloop"]:
                sys.exit(self.spec.variants["impl"].value + "is not supported by this compiler")
        # ===================================
        #               ONEAPI
        # ===================================
        if spec.compiler.name == "oneapi":
            flags = "-std18 -Ofast -xHOST -qopt-zmm-usage=low"
            if config["FC"] == "ifort":
                flags += "-qopt-streaming-stores=always"

            config["DOCONCURRENT_FLAG"] = "-qopenmp" + (
                "-parallel" if config["FC"] == "ifort" else ""
            )
            config["ARRAY_FLAG"] = "-qopenmp" + ("-parallel" if config["FC"] == "ifort" else "")
            config["OPENMP_FLAG"] = "-qopenmp" + (
                "-fopenmp-targets=spir64 -DUSE_FLOAT=1" if config["FC"] == "ifx" else ""
            )

            # Error Messages
            if self.spec.variants["impl"].value in [
                "CUDA",
                "CUDAKernels",
                "OpenACC",
                "OpenACCArray",
            ]:
                sys.exit(self.spec.variants["impl"].value + "is not supported by this compiler")

        # ===================================
        #               FJ
        # ===================================
        if spec.compiler.name == "fj":
            flags = "-X08 -Kfast -KA64FX -KSVE -KARMV8_3_A -Kzfill=100 "
            flags += "-Kprefetch_sequential=soft " 
            flags += "-Kprefetch_line=8 -Kprefetch_line_L2=16 -Koptmsg=2 "
            flags += "-Keval -DUSE_OMP_GET_WTIME=1 "  # FJ Fortran system_clock is low resolution

            config["DOCONCURRENT_FLAG"] = "-Kparallel,reduction -DNOTSHARED"
            config["ARRAY_FLAG"] = "-Kparallel,reduction"
            config["OPENMP_FLAG"] = pkg.compiler.openmp_flag

            # Error Messages
            if self.spec.variants["impl"].value in ["CUDA", "CUDAKernels", "OpenACC"]:
                sys.exit(self.spec.variants["impl"].value + "is not supported by this compiler")

        with open(self.build_directory + "/make.inc." + spec.compiler.name, "w+") as inc:
            for key in config:
                inc.write("{0} = {1}\n".format(key, config[key]))

    def setup_build_environment(self, env):
        ######################################
        # Build and Installation Directories #
        ######################################

        # The environment variable ESMF_DIR must be set to the full pathname
        # of the top level ESMF directory before building the framework.
        env.set("COMPILER", self.spec.compiler.name)
        env.set("IMPLEMENTATION", self.spec.variants["impl"].value)
        # env.set("IMPLEMENTATION_OBJECT",self.spec.variants["impl"].value + "Stream.o")
        print(self.spec.variants["impl"].value)
        print(self.spec.compiler.version)
        print(platform.machine())
        # This creates a testing tree (if one doesn't already exist) and
        # copies the binaries from `src/fortran` to `SpackPackage/bin`.
        # This allows you to use the testing tree independently of the
        # source tree in the future.
        # print(pkg.compiler.cc_pic_flag)

    @property
    def build_name(self):
        compiler_prefix = self.spec.compiler.name
        implementation_prefix = self.spec.variants["impl"].value
        return "{}.{}.{}".format("BabelStream", compiler_prefix, implementation_prefix)

    def install(self, pkg, spec, prefix):
        mkdir(prefix.bin)
        install(self.build_directory + "/" + self.build_name, prefix.bin)
        # To check the make.inc file generated
        install_tree(self.build_directory, prefix.lib)
