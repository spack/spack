# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGimmik(PythonPackage):
    """Generator of Matrix Multiplication Kernels - GiMMiK - is a tool for generation of
    high performance matrix multiplication kernel code.
    for various accelerator platforms."""

    homepage = "https://github.com/PyFR/GiMMiK"
    pypi = "gimmik/gimmik-2.2.tar.gz"

    maintainers("MichaelLaufer")

    license("BSD-3-Clause")

    version(
        "3.0",
        sha256="370c998d127fac64b216e0b3bdc66d27c26b406cb99713f5d52d10eaae87bc1d",
        url="https://pypi.org/packages/77/3a/4909f22d9240d998930c806b109d0b5e448910d63631afd924ffc95d4156/gimmik-3.0-py3-none-any.whl",
    )
    version(
        "2.3",
        sha256="ed4fac8dc39e47bd3090e1618bd909b9b1f83fad7234ab65c715d87b90d5c0c6",
        url="https://pypi.org/packages/fb/76/95b9cf397804a9a9223fd34f531b77cb7a7b4261708fd524156929de9a2c/gimmik-2.3-py3-none-any.whl",
    )
    version(
        "2.2",
        sha256="87a49e02ba1e8d3db55d85ca25ac2604722c87f7252e165f7a9820d20f37908b",
        url="https://pypi.org/packages/e9/0b/c11506535150ed2efbc9bd1e2c5a26c9bc5846f328583dda0c3b1ac6a175/gimmik-2.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-mako", when="@2.2:")
        depends_on("py-numpy@1.7:", when="@2.2:")
