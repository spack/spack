# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import tempfile

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyTensorflowMetadata(PythonPackage):
    """Library and standards for schema and statistics.

    TensorFlow Metadata provides standard representations for metadata that are
    useful when training machine learning models with TensorFlow."""

    homepage = "https://pypi.org/project/tensorflow-metadata/"

    # Only available as a wheel on PyPI
    url = "https://github.com/tensorflow/metadata/archive/refs/tags/v1.5.0.tar.gz"

    license("Apache-2.0")

    version("1.17.1", sha256="6a49a3fac9616336d23c04990e7a8e566d4c97024730e11a7ec7a511c9167e2b")
    version("1.10.0", sha256="e7aa81aa01433e2a75c11425affd55125b64f384baf96b71eeb3a88dca8cf2ae")
    version("1.5.0", sha256="f0ec8aaf62fd772ef908efe4ee5ea3bc0d67dcbf10ae118415b7b206a1d61745")

    with default_args(type="build"):
        depends_on("bazel@6.5:", when="@1.17.1:")
        depends_on("bazel@0.24.1:")
        depends_on("py-setuptools")

    with default_args(type=("build", "run")):
        depends_on("python@3.9:3", when="@1.15:")
        depends_on("python@3.7:3")
        depends_on("py-absl-py@0.9:2", when="@1.15:")
        depends_on("py-absl-py@0.9:1", when="@1.6:1.14")
        depends_on("py-absl-py@0.9:0.12", when="@:1.5")
        depends_on("py-googleapis-common-protos@1.56.4:1", when="@1.15: ^python@3.11:")
        depends_on("py-googleapis-common-protos@1.52:1", when="@:1.14")
        depends_on("py-protobuf@4.25.2:5", when="@1.17: ^python@3.11:")
        depends_on("py-protobuf@4.21.6:4.21", when="@1.17: ^python@:3.10")
        depends_on("py-protobuf@3.13:3", when="@:1.16")

    # Fix non-existing zlib URL
    patch(
        "https://github.com/tensorflow/metadata/commit/8df679e782f5bf2d163d63e550d8752c3812d566.patch?full_index=1",
        sha256="a6b294d5e6099979192fcdb4d5b7b0388dc30b48671944d22e51a9e6bd5e1490",
        when="@1.10.0",
    )

    def patch(self):
        filter_file(
            "self._additional_build_options = ['--copt=-DWIN32_LEAN_AND_MEAN']",
            "self._additional_build_options = ['--copt=-DWIN32_LEAN_AND_MEAN',"
            f" '--jobs={make_jobs}']",
            "setup.py",
            string=True,
        )
        filter_file(
            "self._additional_build_options = []",
            f"self._additional_build_options = ['--jobs={make_jobs}']",
            "setup.py",
            string=True,
        )

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        tmp_path = tempfile.mkdtemp(prefix="spack")
        env.set("TEST_TMPDIR", tmp_path)
