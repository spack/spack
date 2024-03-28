# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import tempfile

from spack.package import *


class PyTensorflowMetadata(PythonPackage):
    """Library and standards for schema and statistics.

    TensorFlow Metadata provides standard representations for metadata that are
    useful when training machine learning models with TensorFlow."""

    homepage = "https://pypi.org/project/tensorflow-metadata/"

    # Only available as a wheel on PyPI
    url = "https://github.com/tensorflow/metadata/archive/refs/tags/v1.5.0.tar.gz"

    license("Apache-2.0")

    version(
        "1.10.0",
        sha256="e3ff528496105c0d73b2a402877525b1695635378fbe5c1b47ac7b3780816bb3",
        url="https://pypi.org/packages/3a/86/2b3251bb560068f31817d9b678588098e28f396c1f6b88c57cf5d28670af/tensorflow_metadata-1.10.0-py3-none-any.whl",
    )
    version(
        "1.5.0",
        sha256="982aa5715a306c5fcce0817da49ad0892f5d977db37e1811c34013ba4da06207",
        url="https://pypi.org/packages/81/e6/193d9637b844f88797199fced0e3baa893dd110bdca34b5708b49120ae30/tensorflow_metadata-1.5.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-absl-py@0.9:1", when="@1.6:")
        depends_on("py-absl-py@0.9:0.12", when="@0.29:1.5")
        depends_on("py-googleapis-common-protos@1.52:", when="@0.24:")
        depends_on("py-protobuf@3.13.0:3", when="@1.1:1.13.0")

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

    def setup_build_environment(self, env):
        tmp_path = tempfile.mkdtemp(prefix="spack")
        env.set("TEST_TMPDIR", tmp_path)
