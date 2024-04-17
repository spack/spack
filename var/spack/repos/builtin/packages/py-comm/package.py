# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyComm(PythonPackage):
    """Jupyter Python Comm implementation, for usage in ipykernel, xeus-python etc."""

    homepage = "https://github.com/ipython/comm"
    pypi = "comm/comm-0.1.3.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.1.4",
        sha256="6d52794cba11b36ed9860999cd10fd02d6b2eac177068fdd585e1e2f8a96e67a",
        url="https://pypi.org/packages/fe/47/0133ac1b7dc476ed77710715e98077119b3d9bae56b13f6f9055e7da1c53/comm-0.1.4-py3-none-any.whl",
    )
    version(
        "0.1.3",
        sha256="16613c6211e20223f215fc6d3b266a247b6e2641bf4e0a3ad34cb1aff2aa3f37",
        url="https://pypi.org/packages/74/f3/b88d7e1dadf741550c56b70d7ce62673354fddb68e143d193ceb80224208/comm-0.1.3-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-traitlets@4:4.0.0.0,4.1:", when="@0.1.4:")
        depends_on("py-traitlets@5.3:5.3.0.0,5.4:", when="@0.1.2:0.1.3")
