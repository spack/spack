# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGalaxy2cwl(PythonPackage):
    """Convert a Galaxy workflow to abstract Common Workflow Language (CWL)"""

    homepage = "https://github.com/workflowhub-eu/galaxy2cwl"

    version(
        "0.1.4",
        url="https://files.pythonhosted.org/packages/8d/38/79857ee2a38118ef4007311b7cba480b410369333ba004c6d842feadcc77/galaxy2cwl-0.1.4-py3-none-any.whl",
        sha256="b6558272656e6f279948ee76d9863b4c00f467ad59b2d1190ca2304e514f7ce9",
        expand=False,
    )

    depends_on("py-setuptools", type="build")
