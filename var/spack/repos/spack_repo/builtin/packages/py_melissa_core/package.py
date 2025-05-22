# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyMelissaCore(PythonPackage, CudaPackage):
    """Melissa is a file-avoiding, adaptive, fault-tolerant and elastic
    framework, to run large-scale sensitivity analysis or deep-surrogate
    training on supercomputers.
    This package builds the launcher and server modules.
    """

    homepage = "https://gitlab.inria.fr/melissa/melissa"
    git = "https://gitlab.inria.fr/melissa/melissa.git"
    # FIXME: Replace with an official link
    url = "https://gitlab.inria.fr/melissa/melissa/-/archive/ac-develop-stable/melissa-ac-develop-stable.tar.gz"
    maintainers("abhishekp1297", "viperML", "raffino")

    license("BSD-3-Clause")

    version("develop", branch="develop", preferred=True)
    version(
        "joss", tag="JOSS_v2", commit="20bbe68c1a7b73aa2ea3ad35681c332c7a5fc516", deprecated=True
    )
    version("sc23", tag="SC23", commit="8bb5b6817d4abe4eaa5893552d711150e53535f3", deprecated=True)

    # define variants for the deep learning server (torch, tf)
    variant(
        "torch", default=False, description="Install Deep Learning requirements with Pytorch only"
    )
    variant(
        "tf",
        default=True,
        when="~torch",
        description="Install Deep Learning requirements with TensorFlow only",
    )
    # ==============================
    #       Base dependencies
    # ==============================
    depends_on("python@3.9:3.12", type=("build", "run"))
    depends_on("py-setuptools@46.4:", type="build")
    depends_on("py-pyzmq@22.3.0:", type="run")
    depends_on("py-mpi4py@3.1.3:3", type="run")
    depends_on("py-numpy@1.21:1", type="run")
    depends_on("py-jsonschema@4.5:", type="run")
    depends_on("py-python-rapidjson@1.8:", type="run")
    depends_on("py-scipy@1.10.0:1", type="run")
    depends_on("py-plotext@5.2.8:", type="run")
    depends_on("py-cloudpickle@2.2.0:", type="run")
    depends_on("py-iterative-stats@0.1:", type="run")
    depends_on("py-psutil@5:", type="run")
    # ==============================
    #       DL dependencies
    # ==============================
    for framework in ["+tf", "+torch"]:
        conflicts(
            "%gcc@:9",
            when=framework,
            msg=f"GCC must be greater than version 9 when using {framework}",
        )
        depends_on("py-tensorboard@2.10.0:2", type="run", when=framework)
        depends_on("py-matplotlib", type="run", when=framework)
        depends_on("py-pandas", type="run", when=framework)
        # WARNING: If using a gcc compiler, then support with AVX512-VNNI is
        # expected for bazel source builds.
        # The instruction set comes with binutils. If you are installing a gcc
        # through spack then do spack install `gcc+binutils`
        depends_on("binutils@2.29:", type="build", when=f"{framework} %gcc")

    # WARNING: do not change the upper limit for tensorflow beyond 2.17, which requires
    # AVX-VNNI-INT8 support.
    # Check cpu flags to ensure if avxvnniint8 is available on your machine,
    # if you want to increase the upper limit.
    depends_on("py-tensorflow@2.8.0:2.17 ~cuda", type="run", when="+tf ~cuda")
    depends_on("py-torch@1.12.1:2.6 ~cuda", type="run", when="+torch ~cuda")

    # ==============================
    #       CUDA dependencies
    # ==============================
    for arch in CudaPackage.cuda_arch_values:
        # Support beyond ampere (A100) GPUs hasn't been tested yet.
        # FIXME: free to modify and test
        if arch.isdigit() and 60 <= int(arch) <= 80:
            cuda_specs = f"+cuda cuda_arch={arch}"
            depends_on(f"nccl {cuda_specs}", when=cuda_specs)  # it is set by default
            depends_on(
                f"py-tensorflow@2.8.0:2.17 {cuda_specs}", type="run", when=f"+tf {cuda_specs}"
            )
            depends_on(
                f"py-torch@1.12.1:2.6 {cuda_specs}", type="run", when=f"+torch {cuda_specs}"
            )
        else:
            conflicts(
                f"+cuda cuda_arch={arch}",
                msg="Support beyond Ampere GPUs has not been tested yet. "
                "Accepted values are between 60 and 80 inclusive.",
            )
