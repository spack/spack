# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJmp(PythonPackage):
    """JMP is a Mixed Precision library for JAX."""

    homepage = "https://github.com/deepmind/jmp"
    # pypi tarball has requirements.txt missing
    url = "https://github.com/deepmind/jmp/archive/refs/tags/v0.0.2.tar.gz"

    license("Apache-2.0")

    version(
        "0.0.2",
        sha256="48f94b2ba0c9db759851a23cce2fbfa622e954c3c811651bc11b196246f02527",
        url="https://pypi.org/packages/ff/5c/1482f4a4a502e080af2ca54d7f80a60b5d4735f464c151666d583b78c226/jmp-0.0.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-dataclasses@0.7:", when="@0.0.2: ^python@:3.6")
        depends_on("py-numpy@1.19.5:", when="@0.0.2:")
