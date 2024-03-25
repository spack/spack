# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import tempfile

from spack.package import *


class PyJaxlib(PythonPackage, CudaPackage):
    """XLA library for Jax"""

    homepage = "https://github.com/google/jax"
    url = "https://github.com/google/jax/archive/refs/tags/jaxlib-v0.1.74.tar.gz"

    tmp_path = ""
    buildtmp = ""

    license("Apache-2.0")

    version("0.4.25", sha256="fc1197c401924942eb14185a61688d0c476e3e81ff71f9dc95e620b57c06eec8")
    version("0.4.24", sha256="c4e6963c2c36f634a9a1765e476a1ed4e6c4a7954465ebf72e29f344c28ddc28")
    version("0.4.16", sha256="85c8bc050abe0a2cf62e8cfc7edb4904dd3807924b5714ec6277f291c576b5ca")
    version("0.4.3", sha256="2104735dc22be2b105e5517bd5bc6ae97f40e8e9e54928cac1585c6112a3d910")
    version(
        "0.3.22",
        sha256="680a6f5265ba26d5515617a95ae47244005366f879a5c321782fde60f34e6d0d",
        deprecated=True,
    )
    version(
        "0.1.74",
        sha256="bbc78c7a4927012dcb1b7cd135c7521f782d7dad516a2401b56d3190f81afe35",
        deprecated=True,
    )

    variant("cuda", default=True, description="Build with CUDA")

    # build/build.py
    depends_on("py-build", when="@0.4.14:", type="build")

    # jaxlib/setup.py
    depends_on("python@3.9:", when="@0.4.14:", type=("build", "run"))
    depends_on("python@3.8:", when="@0.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-scipy@1.9:", when="@0.4.19:", type=("build", "run"))
    depends_on("py-scipy@1.7:", when="@0.4.7:", type=("build", "run"))
    depends_on("py-scipy@1.5:", type=("build", "run"))
    depends_on("py-numpy@1.22:", when="@0.4.14:", type=("build", "run"))
    depends_on("py-numpy@1.21:", when="@0.4.7:", type=("build", "run"))
    depends_on("py-numpy@1.20:", when="@0.3:", type=("build", "run"))
    depends_on("py-numpy@1.18:", type=("build", "run"))
    depends_on("py-ml-dtypes@0.2:", when="@0.4.14:", type=("build", "run"))
    depends_on("py-ml-dtypes@0.1:", when="@0.4.9:", type=("build", "run"))
    depends_on("py-ml-dtypes@0.0.3:", when="@0.4.7:", type=("build", "run"))

    # .bazelversion
    depends_on("bazel@6.1.2", when="@0.4.11:", type="build")
    depends_on("bazel@5.1.1", when="@0.3.7:0.4.10", type="build")
    depends_on("bazel@5.1.0", when="@0.3.5", type="build")
    depends_on("bazel@5.0.0", when="@0.3.0:0.3.2", type="build")
    depends_on("bazel@4.2.1", when="@0.1.75:0.1.76", type="build")
    depends_on("bazel@4.1.0", when="@0.1.70:0.1.74", type="build")

    # README.md
    depends_on("cuda@11.4:", when="@0.4:+cuda")
    depends_on("cuda@11.1:", when="@0.3+cuda")
    # https://github.com/google/jax/issues/12614
    depends_on("cuda@11.1:11.7.0", when="@0.1+cuda")
    depends_on("cudnn@8.2:", when="@0.4:+cuda")
    depends_on("cudnn@8.0.5:", when="+cuda")

    # Historical dependencies
    depends_on("py-absl-py", when="@:0.3", type=("build", "run"))
    depends_on("py-flatbuffers@1.12:2", when="@0.1", type=("build", "run"))

    conflicts(
        "cuda_arch=none",
        when="+cuda",
        msg="Must specify CUDA compute capabilities of your GPU, see "
        "https://developer.nvidia.com/cuda-gpus",
    )

    # https://github.com/google/jax/issues/19992
    conflicts("@0.4.16:", when="target=ppc64le:")

    def patch(self):
        self.tmp_path = tempfile.mkdtemp(prefix="spack")
        self.buildtmp = tempfile.mkdtemp(prefix="spack")
        filter_file(
            "build --spawn_strategy=standalone",
            f"""
# Limit CPU workers to spack jobs instead of using all HOST_CPUS.
build --spawn_strategy=standalone
build --local_cpu_resources={make_jobs}
""".strip(),
            ".bazelrc",
            string=True,
        )
        filter_file(
            'f"--output_path={output_path}",',
            'f"--output_path={output_path}",'
            f' "--sources_path={self.tmp_path}",'
            ' "--nohome_rc",'
            ' "--nosystem_rc",'
            f' "--jobs={make_jobs}",',
            "build/build.py",
            string=True,
        )
        build_wheel = join_path("build", "build_wheel.py")
        if self.spec.satisfies("@0.4.14:"):
            build_wheel = join_path("jaxlib", "tools", "build_wheel.py")
        filter_file(
            "args = parser.parse_args()",
            "args, junk = parser.parse_known_args()",
            build_wheel,
            string=True,
        )

    def install(self, spec, prefix):
        args = []
        args.append("build/build.py")
        if "+cuda" in spec:
            args.append("--enable_cuda")
            args.append("--cuda_path={0}".format(self.spec["cuda"].prefix))
            args.append("--cudnn_path={0}".format(self.spec["cudnn"].prefix))
            capabilities = ",".join(
                "{0:.1f}".format(float(i) / 10.0) for i in spec.variants["cuda_arch"].value
            )
            args.append("--cuda_compute_capabilities={0}".format(capabilities))
        args.append(
            "--bazel_startup_options="
            "--output_user_root={0}".format(self.wrapped_package_object.buildtmp)
        )
        python(*args)
        with working_dir(self.wrapped_package_object.tmp_path):
            args = std_pip_args + ["--prefix=" + self.prefix, "."]
            pip(*args)
        remove_linked_tree(self.wrapped_package_object.tmp_path)
        remove_linked_tree(self.wrapped_package_object.buildtmp)
