# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import tempfile

from spack.pkgkit import *


class PyTensorflowMetadata(PythonPackage):
    """Library and standards for schema and statistics.

    TensorFlow Metadata provides standard representations for metadata that are
    useful when training machine learning models with TensorFlow."""

    homepage = "https://pypi.org/project/tensorflow-metadata/"

    # Only available as a wheel on PyPI
    url = "https://github.com/tensorflow/metadata/archive/refs/tags/v1.5.0.tar.gz"

    version(
        "1.5.0",
        sha256="f0ec8aaf62fd772ef908efe4ee5ea3bc0d67dcbf10ae118415b7b206a1d61745",
    )

    depends_on("bazel@0.24.1:", type="build")
    depends_on("python@3.7:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-absl-py@0.9:0.12", type=("build", "run"))
    depends_on("py-googleapis-common-protos@1.52.0:1", type=("build", "run"))
    depends_on("py-protobuf@3.13:3", type=("build", "run"))

    def setup_build_environment(self, env):
        tmp_path = tempfile.mkdtemp(prefix="spack")
        env.set("TEST_TMPDIR", tmp_path)
