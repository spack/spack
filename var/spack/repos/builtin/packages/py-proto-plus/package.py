# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyProtoPlus(PythonPackage):
    """Beautiful, Pythonic protocol buffers."""

    homepage = "https://github.com/googleapis/proto-plus-python"
    pypi = "proto-plus/proto-plus-1.23.0.tar.gz"

    version(
        "1.23.0",
        sha256="a829c79e619e1cf632de091013a4173deed13a55f326ef84f05af6f50ff4c82c",
        url="https://pypi.org/packages/ad/41/7361075f3a31dcd05a6a38cfd807a6eecbfb6dbfe420d922cd400fc03ac1/proto_plus-1.23.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-protobuf@3.19.0:4", when="@1.20.6:")
