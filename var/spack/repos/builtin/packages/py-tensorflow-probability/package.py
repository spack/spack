# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
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

    maintainers("aweits")

    version("0.18.0", sha256="f4852c0fea9117333ccb868f7a2ca75aecf5dd765dc39fd4ee5f8ab6fe87e909")
    version("0.12.1", sha256="1fe89e85fd053bf36e8645a5a1a53b729bc254cf1516bc224fcbd1e4ff50083a")
    version(
        "0.8.0",
        sha256="f6049549f6d6b82962523a6bf61c40c1d0c7ac685f209c0084a6da81dd78181d",
        url="https://github.com/tensorflow/probability/archive/0.8.0.tar.gz",
    )

    extends("python")
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
    depends_on("py-tensorflow@2.10:", when="@0.18:", type=("build", "run"))
    depends_on("py-tensorflow@2.4:", when="@0.12:", type=("build", "run"))
    depends_on("py-tensorflow@1.14:", when="@0.8:", type=("build", "run"))

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
