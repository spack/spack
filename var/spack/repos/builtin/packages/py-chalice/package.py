# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyChalice(PythonPackage):
    """Python Serverless Microframework for AWS."""

    homepage = "https://github.com/aws/chalice"
    url = "https://github.com/aws/chalice/archive/1.20.0.tar.gz"

    license("Apache-2.0")

    version(
        "1.20.0",
        sha256="607514b073dfc914ace44bd192ba96a227ec7c8ad7f147c147c23fa0f3dc6776",
        url="https://pypi.org/packages/1e/f5/9a18fe259700ea6635d18296c248142e207b1d84d0ae7bc631fbb678a856/chalice-1.20.0-py2.py3-none-any.whl",
    )
    version(
        "1.19.0",
        sha256="0229eb7749209f353e266aeddac344dfef1df6752a8e4307dfbfc5d5f98c3b66",
        url="https://pypi.org/packages/29/ed/b0a174eca4f26a1d5825774304db4bc7fc216e2305cab22e21b67d728015/chalice-1.19.0-py2.py3-none-any.whl",
    )
    version(
        "1.18.1",
        sha256="d18aeb83898f4d15bea822e07d862baad375b6507f9a7aa327399d163a5d328e",
        url="https://pypi.org/packages/eb/31/c36deff94d5acb3c5acf8654796f8fa40f5685b383c5d721f43c75510fd2/chalice-1.18.1-py2.py3-none-any.whl",
    )
    version(
        "1.18.0",
        sha256="a2787833bd8acaca66e18b67752921b3eac61efc7a38f8c047746aa35a3723bd",
        url="https://pypi.org/packages/50/5e/54e2fe7ce6bb797b44de1cf3963a32d10e3bdc763cf9492f41ed6dd087b1/chalice-1.18.0-py2.py3-none-any.whl",
    )
    version(
        "1.17.0",
        sha256="6b8200200ece65ee76857c46cfe033d678ffe66685eba00c44fdb38be571d647",
        url="https://pypi.org/packages/8c/64/a8bcd63117a4dfed256f9b88c430e2bade31349ef8def2fd972aab812327/chalice-1.17.0-py2.py3-none-any.whl",
    )
    version(
        "1.16.0",
        sha256="73dc0054421fad23bc4ad5e18eb08da220c71de60f1732df486dba085a5413ff",
        url="https://pypi.org/packages/5a/13/e2336421984c28392c864256c1b7f1faa0bdcb725b0fabd841512e667c3e/chalice-1.16.0-py2.py3-none-any.whl",
    )
    version(
        "1.15.1",
        sha256="9e4c000b8e8f6a5286fb0895904f2c82e1975bb60cd5df745807421c36820ce6",
        url="https://pypi.org/packages/6c/75/773e920859614bffcbbc9b3c6fedc99088e10fe8e4e992aca94335eeb9a7/chalice-1.15.1-py2.py3-none-any.whl",
    )
    version(
        "1.14.1",
        sha256="1602c8051341d09e01bd20de78d97c9324dc0606b53fc5c9fb96c2a1cf070331",
        url="https://pypi.org/packages/7d/71/3768159418fcd25ed3dc2a2116d14436caf2fac5b4f776ef1c61266b7c21/chalice-1.14.1-py2.py3-none-any.whl",
    )
    version(
        "1.14.0",
        sha256="889ee5e58a05037fc1582f556bc612e1683971db79d72d5aa8d961b39ef78bc6",
        url="https://pypi.org/packages/5b/97/07aef5b7f5944486c7bc104c59480ed478688c29a6d468f90da46017714b/chalice-1.14.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-attrs@19.3:19", when="@1.13:1.20.0")
        depends_on("py-botocore@1.12.86:", when="@1.8:1.22")
        depends_on("py-click@7", when="@1.17:1.24.1")
        depends_on("py-click@6.6:7", when="@1.11.1:1.16")
        depends_on("py-enum-compat@0.0.2:", when="@1.6:1.22.1")
        depends_on("py-jmespath@0.9.3:0", when="@1.2:1.26")
        depends_on("py-mypy-extensions@0.4.3", when="@1.15:1.27.2")
        depends_on("py-pip@9:20.2", when="@1.17:1.21.4")
        depends_on("py-pip@9:20.1", when="@1.14.1:1.16")
        depends_on("py-pip@9:20.0", when="@1.13:1.14.0")
        depends_on("py-pyyaml@5.3.1:5", when="@1.15:1.26.1")
        depends_on("py-setuptools", when="@1.6.1:")
        depends_on("py-six@1.10:", when="@1.0.2:")
        depends_on("py-wheel", when="@1.6.1:")
