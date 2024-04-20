# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import tempfile

from spack.package import *


class PyTfKeras(PythonPackage):
    """The TF-Keras library is a pure TensorFlow implementation of Keras,
    based on the legacy tf.keras codebase. Note that the "main" version
    of Keras is now Keras 3 (formerly Keras Core), which is a
    multi-backend implementation of Keras, supporting JAX, PyTorch, and TensorFlow.
     Keras 3 is being developed at keras-team/keras."""

    homepage = "https://github.com/keras-team/tf-keras"
    url = "https://github.com/keras-team/tf-keras/archive/refs/tags/v2.16.0.tar.gz"

    maintainers("jonas-eschle")

    license("Apache-2.0", checked_by="jonas-eschle")

    max_minor = 16
    version("2.16.0", sha256="b98fa4d75c325c44aade329ac4269ab93515b308624854edbacf1cef707207da")

    # Supported Python versions listed in multiple places:
    # * tf-keras/tools/pip_package/setup.py
    # * CONTRIBUTING.md
    # * PKG-INFO
    depends_on("python@3.9:", type=("build", "run"), when="@2.16:")
    depends_on("py-setuptools", type="build")

    # Required dependencies listed in multiple places:
    # * BUILD
    # * WORKSPACE
    depends_on("py-absl-py", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("pil", type=("build", "run"))
    depends_on("py-portpicker", type=("build", "run"))
    depends_on("py-pydot", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    # the tf-keras versions are following along with TF versions
    for minor_ver in range(16, max_minor + 1):
        depends_on(
            "py-tensorflow@2.{}".format(minor_ver),
            type=("build", "run"),
            when="@2.{}".format(minor_ver),
        )
        depends_on(
            "py-tensorboard@2.{}".format(minor_ver),
            type=("build", "run"),
            when="@2.{}".format(minor_ver),
        )
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("bazel", type="build")
    depends_on("protobuf", type="build")

    def patch(self):
        infile = join_path(self.package_dir, "protobuf_build.patch")
        with open(infile, "r") as source_file:
            text = source_file.read()
        with open("tf_keras/keras.bzl", mode="a") as f:
            f.write(text)

        filter_file(
            'load("@com_google_protobuf//:protobuf.bzl", "py_proto_library")',
            'load("@org_keras//tf_keras:keras.bzl", "py_proto_library")',
            "tf_keras/protobuf/BUILD",
            string=True,
        )

    def install(self, spec, prefix):
        self.tmp_path = tempfile.mkdtemp(prefix="spack")
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
            "//tf_keras/tools/pip_package:build_pip_package",
        ]

        bazel(*args)

        build_pip_package = Executable("bazel-bin/tf-keras/tools/pip_package/build_pip_package")
        buildpath = join_path(self.stage.source_path, "spack-build")
        build_pip_package("--src", buildpath)

        with working_dir(buildpath):
            args = std_pip_args + ["--prefix=" + prefix, "."]
            pip(*args)
        remove_linked_tree(self.tmp_path)
