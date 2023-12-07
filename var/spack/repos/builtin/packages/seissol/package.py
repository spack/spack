# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Seissol(CMakePackage, CudaPackage):
    """Seissol - A scientific software for the numerical simulation
    of seismic wave phenomena and earthquake dynamics.
    """

    homepage = "http://www.seissol.org"
    git = "https://github.com/SeisSol/SeisSol.git"
    version("master", branch="master", submodules=True)
    # we cannot use the tar.gz file because it does not contains submodules
    version(
        "1.1.2", tag="v1.1.2", commit="71002c1c1498ebd6f50a954731da68fa4f9d436b", submodules=True
    )

    maintainers("Thomas-Ulrich", "ravil-mobile", "davschnellerkrenzland")

    variant("asagi", default=True, description="installs asagi for material input")
    variant(
        "convergence_order",
        default="4",
        description="polynomial degree plus one",
        values=(str(v) for v in range(2, 9)),
        multi=False,
    )
    variant(
        "precision",
        default="double",
        description="float numerical precision",
        values=("single", "double"),
        multi=False,
    )
    variant(
        "dr_quad_rule",
        default="stroud",
        description="dynamic rupture quadrature rule",
        values=("stroud", "dunavant"),
        multi=False,
    )
    variant(
        "equations",
        default="elastic",
        description="equation set used",
        values=("elastic", "anisotropic", "viscoelastic2", "poroelastic"),
        multi=False,
    )
    variant(
        "number_of_mechanisms", default="3", description="number of mechanisms for viscoelasticity"
    )
    variant(
        "device_backend",
        default="none",
        description="type of gpu backend",
        values=("none", "cuda", "hip", "hipsycl", "oneapi"),
        multi=False,
    )
    # minus are used because coma would be interpreted as multiple values
    variant(
        "gemm_tools",
        default="auto",
        description="gemm tool(s) for the code generator",
        values=(
            "auto",
            "LIBXSMM-PSpaMM",
            "LIBXSMM",
            "MKL",
            "OpenBLAS",
            "BLIS",
            "PSpaMM",
            "Eigen",
            "LIBXSMM-PSpaMM-GemmForge",
            "Eigen-GemmForge",
            "LIBXSMM_JIT-PSpaMM",
            "LIBXSMM_JIT",
            "LIBXSMM_JIT-PSpaMM-GemmForge",
        ),
        multi=False,
    )

    variant("mpi", default=True, description="installs an MPI implementation")
    variant("libxsmm", default=True, description="installs libxsmm-generator")
    variant("memkind", default=True, description="Use memkind library for hbw memory support")

    conflicts(
        "cuda_arch=none",
        when="+cuda",
        msg="A value for cuda_arch must be specified. Add cuda_arch=XX",
    )

    conflicts(
        "device_backend=none",
        when="+cuda",
        msg="A value for device_backend must be specified. Add device_backend=XX",
    )

    variant("python", default=False, description="installs python, pip, numpy and scipy")

    depends_on("mpi", when="+mpi")
    # with cuda 12 and llvm 14:15, we have the issue: "error: no template named 'texture"
    # https://github.com/llvm/llvm-project/issues/61340
    conflicts("cuda@12", when="+cuda ^llvm@14:15")
    # this issue is fixed with llvm 16. SeisSol compiles but does not run on heisenbug:
    # [hipSYCL Warning] from (...)/cuda_hardware_manager.cpp:55 @ cuda_hardware_manager():
    # cuda_hardware_manager: Could not obtain number of devices (error code = CUDA:35)
    # [hipSYCL Error] from (...)/cuda_hardware_manager.cpp:74 @ get_device():
    # cuda_hardware_manager: Attempt to access invalid device detected.
    # Therefore the cuda version is set to 11 now, but this constrain could be released in the future
    depends_on("cuda@11", when="+cuda")

    depends_on("hipsycl@develop +cuda", when="+cuda")

    depends_on("parmetis +int64 +shared", when="+mpi")
    depends_on("metis +int64 +shared", when="+mpi")
    depends_on("libxsmm@1.17 +generator", when="+libxsmm target=x86_64:")

    depends_on("hdf5@1.10:1.12.2 +shared +threadsafe ~mpi", when="~mpi")
    depends_on("hdf5@1.10:1.12.2 +shared +threadsafe +mpi", when="+mpi")

    depends_on("netcdf-c@4.6:4.7.4 +shared ~mpi", when="~mpi")
    depends_on("netcdf-c@4.6:4.7.4 +shared +mpi", when="+mpi")

    depends_on("asagi ~mpi ~mpi3 ~fortran", when="+asagi ~mpi")
    depends_on("asagi +mpi +mpi3", when="+asagi +mpi")

    depends_on("easi@1.2 ~asagi jit=impalajit,lua", when="~asagi")
    depends_on("easi@1.2 +asagi jit=impalajit,lua", when="+asagi")

    depends_on("intel-mkl threads=none", when="gemm_tools=MKL")
    depends_on("blis threads=none", when="gemm_tools=BLIS")
    depends_on("openblas threads=none", when="gemm_tools=OpenBLAS")
    depends_on("memkind", when="+memkind target=x86_64:")

    depends_on("py-pspamm")
    depends_on("yaml-cpp@0.6.2")
    depends_on("cxxtest")
    depends_on("eigen@3.4.0")

    """
    depends_on("py-numpy", when="+python")
    depends_on("py-scipy", when="+python")
    depends_on("py-matplotlib", when="+python")
    depends_on("py-pyopenssl", when="+python")
    """

    depends_on("python@3")

    def cmake_args(self):
        args = [
            self.define_from_variant("ASAGI", "asagi"),
            self.define_from_variant("PRECISION", "precision"),
            self.define_from_variant("DR_QUAD_RULE", "dr_quad_rule"),
            self.define_from_variant("ORDER", "convergence_order"),
            self.define_from_variant("EQUATIONS", "equations"),
        ]
        gemm_tools = self.spec.variants["gemm_tools"].value.replace("-", ",")
        args.append(f"-DGEMM_TOOLS={gemm_tools}")

        if self.spec.variants["equations"].value != "viscoelastic2":
            args.append("-DNUMBER_OF_MECHANISMS=0")
        else:
            args.append(self.define_from_variant("NUMBER_OF_MECHANISMS", "number_of_mechanisms"))

        if "+cuda" in self.spec:
            cuda_arch = self.spec.variants["cuda_arch"].value[0]
            args.append(f"-DDEVICE_ARCH=sm_{cuda_arch}")
            args.append(self.define_from_variant("DEVICE_BACKEND", "device_backend"))

        # TODO: fill the gaps based on
        # https://spack.readthedocs.io/en/latest/basic_usage.html#support-for-specific-microarchitectures
        arch_dic = {}
        arch_dic["westmere"] = "wsm"
        arch_dic["sandybridge"] = "snb"
        arch_dic["haswell"] = "hsw"
        # arch_dic[""] = "knc"
        # arch_dic[""] = "knl"
        arch_dic["skylake_avx512"] = "skx"
        arch_dic["zen"] = "naples"
        arch_dic["zen2"] = "rome"
        arch_dic["zen3"] = "milan"
        arch_dic["zen4"] = "bergamo"
        arch_dic["thunderx2"] = "thunderx2t99"
        arch_dic["power9"] = "power9"
        arch_dic["a64fx"] = "a64fx"
        # arch_dic[""] = "neon"
        # arch_dic[""] = "sve128"
        # arch_dic[""] = "sve256"
        # arch_dic[""] = "sve512"
        # arch_dic[""] = "sve1024"
        # arch_dic[""] = "sve2048"
        arch_dic["m1"] = "apple-m1"
        arch_dic["m2"] = "apple-m2"
        target = str(self.spec.target)
        if target in arch_dic:
            args.append("-DHOST_ARCH=" + arch_dic[target])
        else:
            print(target, "not in arch list of tandem, using noarch")
            args.append("-DARCH=noarch")

        return args

    def setup_run_environment(self, env):
        # for seissol-launch
        env.prepend_path("PATH", self.prefix.share)
