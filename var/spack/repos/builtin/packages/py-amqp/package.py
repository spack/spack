# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAmqp(PythonPackage):
    """Low-level AMQP client for Python (fork of amqplib)."""

    pypi = "amqp/amqp-2.4.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "5.0.9",
        sha256="9cd81f7b023fc04bbb108718fbac674f06901b77bfcdce85b10e2a5d0ee91be5",
        url="https://pypi.org/packages/b9/80/76cc2ce4789c91394f43e0e78d86be5738b5223d106c11d78bacc260a559/amqp-5.0.9-py3-none-any.whl",
    )
    version(
        "5.0.1",
        sha256="a8fb8151eb9d12204c9f1784c0da920476077609fa0a70f2468001e3a4258484",
        url="https://pypi.org/packages/6a/10/2d781823dd1366d7609148714e1a81af402c3c4d0ef52c1a1ac0716da9d0/amqp-5.0.1-py2.py3-none-any.whl",
    )
    version(
        "2.6.1",
        sha256="aa7f313fb887c91f15474c1229907a04dac0b8135822d6603437803424c0aa59",
        url="https://pypi.org/packages/bc/90/bb5ce93521772f083cb2d7a413bb82eda5afc62b4192adb7ea4c7b4858b9/amqp-2.6.1-py2.py3-none-any.whl",
    )
    version(
        "2.5.2",
        sha256="6e649ca13a7df3faacdc8bbb280aa9a6602d22fd9d545336077e573a1f4ff3b8",
        url="https://pypi.org/packages/fc/a0/6aa2a7923d4e82dda23db27711d565f0c4abf1570859f168e3d0975f1eb6/amqp-2.5.2-py2.py3-none-any.whl",
    )
    version(
        "2.4.2",
        sha256="35a3b5006ca00b21aaeec8ceea07130f07b902dd61bfe42815039835f962f5f1",
        url="https://pypi.org/packages/42/ec/cbbaa8f75be8cbd019afb9d63258e2bdc95242f8c46a54bb90db5fef03bd/amqp-2.4.2-py2.py3-none-any.whl",
    )
    version(
        "2.4.1",
        sha256="16056c952e8029ce8db097edf0d7c2fe2ba9de15d30ba08aee2c5221273d8e23",
        url="https://pypi.org/packages/27/32/5c8a0d355b247446eb73f89c0fa4a22c1832764c0cc9d2bc43b9256d9366/amqp-2.4.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-vine@5.0.0:5.0", when="@5.0.1:5.0")
        depends_on("py-vine@1.1.3:1", when="@2.5:2")
        depends_on("py-vine@1.1.3:", when="@2.2:2.4")
