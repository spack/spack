# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import tempfile

from spack.package import *


class PyTensorflowProbability(Package):
    """TensorFlow Probability (TFP) is a Python library built on
    TensorFlow that makes it easy to combine probabilistic models and
    deep learning on modern hardware (TPU, GPU). It's for data
    scientists, statisticians, ML researchers, and practitioners who
    want to encode domain knowledge to understand data and make
    predictions."""

    homepage = "https://www.tensorflow.org/probability"
    url = "https://github.com/tensorflow/probability/archive/v0.12.1.tar.gz"

    maintainers("aweits", "jonas-eschle")

    license("Apache-2.0")

    version("0.23.0", sha256="a00769550da9284acbd69e32a005507153ad39b0c190feca2bbbf6373366cc14")
    version("0.22.1", sha256="9c1203b454aaeb48ac67dea862a411dba6b04f67c1e874e0e83bd1d7f13829a3")
    version("0.22.0", sha256="f9ce55b00c8069246d701c04eaafccde413355f6e76ccf9e549772ecfa0349a4")
    version("0.21.0", sha256="69b7510b38b2e48bcfb9ff570ef598d489e4f1bcbe13276f5dd91c878b8d56d1")
    version("0.20.0", sha256="f0fb9a1f88a36a8f57d4d9cce4f9bf8dfacb6fc7778751729fe3c3067e5a1363")
    version("0.19.0", sha256="b32d2ae211ec727df9791b501839619f5389134bd6d4fe951570f500b0e75f55")
    version("0.18.0", sha256="f4852c0fea9117333ccb868f7a2ca75aecf5dd765dc39fd4ee5f8ab6fe87e909")
    version("0.12.1", sha256="1fe89e85fd053bf36e8645a5a1a53b729bc254cf1516bc224fcbd1e4ff50083a")
    version(
        "0.8.0",
        sha256="f6049549f6d6b82962523a6bf61c40c1d0c7ac685f209c0084a6da81dd78181d",
        url="https://github.com/tensorflow/probability/archive/0.8.0.tar.gz",
    )

    extends("python@3.9:", when="@0.22:")
    extends("python@3.8:", when="@0.20:0.21")
    extends("python@3.7:", when="@0.13:0.19")
    extends("python@3.6:", when="@0.8:0.12")
    depends_on("py-pip", type="build")
    depends_on("py-wheel", type="build")
    depends_on("py-setuptools", type="build")

    # required_packages.py
    depends_on("py-absl-py", when="@0.18:", type=("build", "run"))
    depends_on("py-six@1.10:", type=("build", "run"))
    depends_on("py-numpy@1.13.3:", type=("build", "run"))
    depends_on("py-decorator", type=("build", "run"))
    depends_on("py-cloudpickle@1.3:", when="@0.12:", type=("build", "run"))
    depends_on("py-cloudpickle@1.1.1", when="@0.8", type=("build", "run"))
    depends_on("py-gast@0.3.2:", when="@0.12:", type=("build", "run"))
    depends_on("py-gast@0.2", when="@0.8", type=("build", "run"))
    depends_on("py-dm-tree", when="@0.12:", type=("build", "run"))

    # tensorflow_probability/python/__init__.py
    # TODO: reactivate the JAX versions once the JAX package is available with newer versions, also add jaxlib
    depends_on("py-tensorflow@2.15", when="@0.23", type=("build", "run"))
    # depends_on("py-jax@0.4.20:0.4", when="@0.23", type=("build", "run"))

    depends_on("py-tensorflow@2.14", when="@0.22", type=("build", "run"))
    # depends_on("py-jax@0.4.16:0.4", when="@0.22", type=("build", "run"))

    depends_on("py-tensorflow@2.13", when="@0.21", type=("build", "run"))
    # depends_on("py-jax@0.4.14:0.4", when="@0.21", type=("build", "run"))

    depends_on("py-tensorflow@2.12", when="@0.20", type=("build", "run"))
    # depends_on("py-jax@0.4.8:0.4", when="@0.20", type=("build", "run"))

    depends_on("py-tensorflow@2.11", when="@0.19", type=("build", "run"))
    depends_on("py-jax@0.3.25", when="@0.19", type=("build", "run"))

    depends_on("py-tensorflow@2.10:", when="@0.18", type=("build", "run"))
    depends_on("py-tensorflow@2.4:", when="@0.12:0.17", type=("build", "run"))
    depends_on("py-tensorflow@1.14:", when="@0.8:0.11", type=("build", "run"))

    depends_on("bazel@3.2:", type="build")

    def install(self, spec, prefix):
        self.tmp_path = tempfile.mkdtemp(prefix="spack")
        env["TEST_TMPDIR"] = self.tmp_path
        env["HOME"] = self.tmp_path

        args = [
            # Don't allow user or system .bazelrc to override build settings
            "--nohome_rc",
            "--nosystem_rc",
            # Bazel does not work properly on NFS, switch to /tmp
            "--output_user_root=" + self.tmp_path,
            "build",
            # Spack logs don't handle colored output well
            "--color=no",
            "--jobs={0}".format(make_jobs),
            # Enable verbose output for failures
            "--verbose_failures",
            "--spawn_strategy=local",
            # bazel uses system PYTHONPATH instead of spack paths
            "--action_env",
            "PYTHONPATH={0}".format(env["PYTHONPATH"]),
            "--copt=-O3",
            "--copt=-march=native",
            ":pip_pkg",
        ]

        bazel(*args)

        with working_dir(join_path("bazel-bin", "pip_pkg.runfiles", "tensorflow_probability")):
            args = std_pip_args + ["--prefix=" + prefix, "."]
            pip(*args)

        remove_linked_tree(self.tmp_path)
