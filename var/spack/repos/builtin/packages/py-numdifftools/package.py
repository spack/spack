# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyNumdifftools(PythonPackage):
    """Solves automatic numerical differentiation problems in one or more
    variables."""

    homepage = "https://github.com/pbrod/numdifftools"
    pypi = "numdifftools/numdifftools-0.9.41.tar.gz"

    version(
        "0.9.41",
        sha256="a8b162e06889ea73643a47b84935a63d8214d4b4b0805d36a3c28c56379b3e51",
        url="https://pypi.org/packages/a3/5c/37cd5db8c465db2664b2219410b8bc7743da6edb1b616b5d13008bd7cac2/numdifftools-0.9.41-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-numpy@1.9:", when="@0.9.13:0.9.16,0.9.20,0.9.40:")
        depends_on("py-scipy", when="@0.9.13:0.9.16,0.9.20,0.9.40:")
