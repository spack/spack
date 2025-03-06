# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class DeepmdLib(CudaPackage, ROCmPackage, CMakePackage):
    """DeePMD-kit is a package written in Python/C++, designed to minimize the effort
    required to build deep learning-based models of interatomic potential energy
    and force field and to perform molecular dynamics (MD)"""

    homepage = "https://docs.deepmodeling.com/projects/deepmd/en/stable/index.html#"
    git = "https://github.com/deepmodeling/deepmd-kit.git"
    url = "https://github.com/deepmodeling/deepmd-kit/archive/refs/tags/v2.2.11.tar.gz"

    license("LGPL-3.0-only")

    maintainers("mtaillefumier")

    version("3.0.2", sha256="b828d3a44730ea852505abbdb24ea5b556f2bf8b16de5a9c76018ed1ced7121b")
    version("3.0.1", sha256="e842edbc2714bc948ce708c411e5fed751e67c88d5c493c2978f11c849027dca")
    version("3.0.0", sha256="4df1091ce90dbea87734a20c6d826b8cbe80ac44646cb592c2e8586be319023c")
    version("3.0.0b0", sha256="44e5a6255f7890f4b9f1cc5e1525380c1d1e41dd75ac9e738d5b81a728759bba")
    version("3.0.0a0", sha256="36e9dc1b18313139b1e9482e06ec214e15a87ee74f5f9d565b8719998e088920")
    version("2.2.11", sha256="d22893a08c2556c5cb29682378105849cf672545c91ee52b10a97da6e9075ac3")

    variant(
        "tensorflow", default=True, description="Enable tensorflow support (original ML backend)"
    )
    variant(
        "pytorch",
        default=False,
        description="Enable pytorch support (starting v3.0.0)",
        when="@3.0:",
    )
    variant("cuda", default=False, description="Enable cuda support")
    variant("rocm", default=False, description="Enable rocm support")
    variant("gromacs", default=False, description="Enable gromacs plugins")
    variant("horovod", default=True, description="Enable horovod support")
    variant("jax", default=False, description="Enable JaX support", when="@3.0:")
    variant("fp64", default=True, description="Enable double precision ops", when="+tensorflow")
    variant("fp64", default=False, description="Enable double precision ops", when="+pytorch")
    # deepmd library uses cmake as a build system but deepmd itself uses pip.

    # Historical dependencies
    depends_on("py-setuptools", type="build")
    depends_on("py-tensorflow@2.16:", when="+tensorflow")
    depends_on("py-tensorflow+mpi", when="+tensorflow")
    depends_on("py-torch", when="+pytorch")
    #depends_on("py-ase")
    #depends_on("py-scipy")
    #depends_on("py-numpy")
    #depends_on("py-pyyaml")
    #depends_on("py-args")
    #depends_on("py-pyproject-metadata")
    #depends_on("py-python-hostlist@1.21:")
    #depends_on("py-typing-extensions", when="^python@:3.8")
    #depends_on("py-importlib-metadata", when="^python@:3.8")
    #depends_on("py-sphinx-argparse")
    #depends_on("py-pygments")
    #depends_on("py-sphinxcontrib-bibtex")
    #depends_on("py-scikit-build-core")
    #depends_on("py-setuptools-scm")
    #depends_on("py-scikit-build")
    #depends_on("py-hatch-fancy-pypi-readme")
    #depends_on("py-pip", type="build")
    #depends_on("python@3.10:")
    #depends_on("py-h5py")
    depends_on("py-jax", when="+jax")

    # horovod needs some special settings
    #depends_on("py-horovod controllers=mpi", when="+horovod")
    #depends_on("py-horovod frameworks=tensorflow", when="+tensorflow+horovod")
    #depends_on("py-horovod frameworks=pytorch", when="+pytorch+horovod")

    # we can install deepmd with tensorflow, py-torch and jax

    with when("+cuda"):
        depends_on("nccl")
     #   depends_on("py-horovod+cuda tensor_ops=nccl", when="+horovod")
        for target in CudaPackage.cuda_arch_values:
            depends_on(f"nccl cuda_arch={target}", when=f"cuda_arch={target}")
      #      depends_on(
      #          f"py-horovod+cuda tensor_ops=nccl cuda_arch={target}",
      #          when=f"+horovod cuda_arch={target}",
      #      )
            depends_on(
                f"py-tensorflow+cuda+nccl+mpi cuda_arch={target}",
                when=f"+tensorflow cuda_arch={target}",
            )
            depends_on(f"py-torch+cuda cuda_arch={target}", when=f"+pytorch cuda_arch={target}")

    with when("+rocm"):
        depends_on("rccl")
       # depends_on("py-horovod+rocm", when="+horovod")
        depends_on("hipcub+rocm")
        depends_on("hip+rocm")

        for target in ROCmPackage.amdgpu_targets:
            depends_on(
                f"py-tensorflow@2.16:+rocm+mpi amdgpu_target={target}",
                when=f"+tensorflow amdgpu_target={target}",
            )
            depends_on(
                f"py-torch+rocm amdgpu_target={target}", when=f"+pytorch amdgpu_target={target}"
            )

    root_cmakelists_dir = "source"

    patch("cmake-patch.diff", when="%gcc@14")

    def setup_build_environment(self, env):
        if "+cuda" in self.spec:
            env.set("DP_VARIANT", "cuda")
        if "+rocm" in self.spec:
            env.set("DP_VARIANT", "rocm")
        if "+tensorflow" in self.spec:
            # turn on double presicion suppport
            env.set("DP_ENABLE_TENSORFLOW", "1")
            # turn off all tensorflow errors, warnings and info messages
            env.set("TF_CPP_MIN_LOG_LEVEL", "3")
            env.set("TENSORFLOW_ROOT", self.spec["py-tensorflow"].prefix)
        if "+pytorch" in self.spec:
            env.set("DP_ENABLE_PYTORCH", "1")

    def cmake_args(self):
        spec = self.spec
        args = [
            self.define_from_variant("USE_CUDA_TOOLKIT", "cuda"),
            self.define_from_variant("USE_ROCM_TOOLKIT", "rocm"),
            self.define_from_variant("ENABLE_TENSORFLOW", "tensorflow"),
            self.define_from_variant("ENABLE_PYTORCH", "pytorch"),
            self.define_from_variant("USE_TF_PYTHON_LIBS", "tensorflow"),
            self.define_from_variant("ENABLE_JAX", "jax"),
        ]

        if "+rocm" in spec:
            args += [self.define_from_variant("TENSORFLOW_USE_ROCM", "tensorflow")]
        return args
