# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyrr(PythonPackage):
    """3D mathematical functions using NumPy."""

    homepage = "https://github.com/adamlwgriffiths/Pyrr"
    pypi = "pyrr/pyrr-0.10.3.tar.gz"
    maintainers("JeromeDuboisPro")

    license("Unlicense")

    version(
        "0.10.3",
        sha256="d8af23fb9bb29262405845e1c98f7339fbba5e49323b98528bd01160a75c65ac",
        url="https://pypi.org/packages/80/d4/09bb74e93f9f677eadcf9ddb92681755f75e0f354a1b904f1913e32ca1b2/pyrr-0.10.3-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-multipledispatch", when="@0.9:")
        depends_on("py-numpy", when="@0.9:")
