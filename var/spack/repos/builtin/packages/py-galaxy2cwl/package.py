# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGalaxy2cwl(PythonPackage):
    """Convert a Galaxy workflow to abstract Common Workflow Language (CWL)"""

    homepage = "https://github.com/workflowhub-eu/galaxy2cwl"
    url = "https://github.com/workflowhub-eu/galaxy2cwl/archive/refs/tags/0.1.4.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.1.4",
        sha256="b6558272656e6f279948ee76d9863b4c00f467ad59b2d1190ca2304e514f7ce9",
        url="https://pypi.org/packages/8d/38/79857ee2a38118ef4007311b7cba480b410369333ba004c6d842feadcc77/galaxy2cwl-0.1.4-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@:3")
        depends_on("py-gxformat2@0.11:")
        depends_on("py-pyyaml@5.3:")
