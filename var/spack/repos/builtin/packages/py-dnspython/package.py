# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDnspython(PythonPackage):
    """DNS toolkit"""

    homepage = "https://www.dnspython.org"
    pypi = "dnspython/dnspython-2.2.1.tar.gz"

    license("ISC")

    version(
        "2.2.1",
        sha256="a851e51367fb93e9e1361732c1d60dab63eff98712e503ea7d92e6eccb109b4f",
        url="https://pypi.org/packages/9b/ed/28fb14146c7033ba0e89decd92a4fa16b0b69b84471e2deab3cc4337cc35/dnspython-2.2.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@:3", when="@2.2")
