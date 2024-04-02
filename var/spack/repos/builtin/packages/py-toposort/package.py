# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyToposort(PythonPackage):
    """Implements a topological sort algorithm."""

    pypi = "toposort/toposort-1.10.tar.gz"

    maintainers("marcusboden")

    license("Apache-2.0")

    version(
        "1.10",
        sha256="cbdbc0d0bee4d2695ab2ceec97fe0679e9c10eab4b2a87a9372b929e70563a87",
        url="https://pypi.org/packages/f6/17/57b444fd314d5e1593350b9a31d000e7411ba8e17ce12dc7ad54ca76b810/toposort-1.10-py3-none-any.whl",
    )
    version(
        "1.9",
        sha256="9f434c815e1bd2f9ad05152b6b0071b1f56e288c107869708f2463ec932e2637",
        url="https://pypi.org/packages/ba/d8/494820a2dc0c03ea8594011b9dac352125c0bd26d5d9db5852fb1663d4b1/toposort-1.9-py3-none-any.whl",
    )
    version(
        "1.8",
        sha256="c87fd1a8d70b2ca8c928eaf90a538307171fed89e1dcfcdbf7cf6599dfc3208a",
        url="https://pypi.org/packages/65/21/bc63063c1d5245c427471aa3ad93b3b5339a5cc139b02c7e43ea18ad65b0/toposort-1.8-py3-none-any.whl",
    )
    version(
        "1.7",
        sha256="8ed8e109e96ae30bf66da2d2155e4eb9989d9c5c743c837e37d9774a4eddd804",
        url="https://pypi.org/packages/0b/d1/dfbff7af958d31a0132ecffe5333ffb5ebb315cdff4a22b4f754bc888aad/toposort-1.7-py2.py3-none-any.whl",
    )
    version(
        "1.6",
        sha256="2ade83028dd067a1d43c142469cbaf4136b92fdc1c4303f16c40f126442fdaf3",
        url="https://pypi.org/packages/f2/7d/55784e894ee0cde2474fb977ffd1651e74e840a9f92e1d847f7e3115d5ec/toposort-1.6-py2.py3-none-any.whl",
    )
