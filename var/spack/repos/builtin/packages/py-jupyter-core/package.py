# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterCore(PythonPackage):
    """Core Jupyter functionality"""

    homepage = "https://jupyter-core.readthedocs.io/"
    pypi = "jupyter-core/jupyter_core-4.6.0.tar.gz"
    git = "https://github.com/jupyter/jupyter_core.git"

    license("BSD-3-Clause")

    version(
        "5.3.0",
        sha256="d4201af84559bc8c70cead287e1ab94aeef3c512848dde077b7684b54d67730d",
        url="https://pypi.org/packages/41/1e/92a67f333b9335f04ce409799c030dcfb291712658b9d9d13997f7c91e5a/jupyter_core-5.3.0-py3-none-any.whl",
    )
    version(
        "5.1.0",
        sha256="f5740d99606958544396914b08e67b668f45e7eff99ab47a7f4bcead419c02f4",
        url="https://pypi.org/packages/ba/88/c829e2cef67fa173ab512a054d1ba7047c2559b311e9f9e7c55b0a9d8278/jupyter_core-5.1.0-py3-none-any.whl",
    )
    version(
        "4.11.1",
        sha256="715e22bb6cc7db3718fddfac1f69f1c7e899ca00e42bdfd4bf3705452b9fd84a",
        url="https://pypi.org/packages/66/5f/32ee101e07d5ece26876f13526b16179525e19f4e460f8085e9ef8e54cff/jupyter_core-4.11.1-py3-none-any.whl",
    )
    version(
        "4.9.2",
        sha256="f875e4d27e202590311d468fa55f90c575f201490bd0c18acabe4e318db4a46d",
        url="https://pypi.org/packages/60/7d/bee50351fe3ff6979e949b9c4c00c556a7a9732ba39b547d07d93450de23/jupyter_core-4.9.2-py3-none-any.whl",
    )
    version(
        "4.7.1",
        sha256="8c6c0cac5c1b563622ad49321d5ec47017bd18b94facb381c6973a0486395f8e",
        url="https://pypi.org/packages/53/40/5af36bffa0af3ac71d3a6fc6709de10e4f6ff7c01745b8bc4715372189c9/jupyter_core-4.7.1-py3-none-any.whl",
    )
    version(
        "4.6.3",
        sha256="a4ee613c060fe5697d913416fc9d553599c05e4492d58fac1192c9a6844abb21",
        url="https://pypi.org/packages/63/0d/df2d17cdf389cea83e2efa9a4d32f7d527ba78667e0153a8e676e957b2f7/jupyter_core-4.6.3-py2.py3-none-any.whl",
    )
    version(
        "4.6.1",
        sha256="464769f7387d7a62a2403d067f1ddc616655b7f77f5d810c0dd62cb54bfd0fb9",
        url="https://pypi.org/packages/fb/82/86437f661875e30682e99d04c13ba6c216f86f5f6ca6ef212d3ee8b6ca11/jupyter_core-4.6.1-py2.py3-none-any.whl",
    )
    version(
        "4.6.0",
        sha256="1368a838bba378c3c99f54c2961489831ea929ec7689a1d59d9844e584bc27dc",
        url="https://pypi.org/packages/56/a6/fe4b7029d4994870df6685bdc7bae5417bea30b627c4ce36106f9cac31fc/jupyter_core-4.6.0-py2.py3-none-any.whl",
    )
    version(
        "4.4.0",
        sha256="927d713ffa616ea11972534411544589976b2493fc7e09ad946e010aa7eb9970",
        url="https://pypi.org/packages/1d/44/065d2d7bae7bebc06f1dd70d23c36da8c50c0f08b4236716743d706762a8/jupyter_core-4.4.0-py2.py3-none-any.whl",
    )
    version(
        "4.2.0",
        sha256="0a168fb999e27f909900893bf14a7b7dc16ee7445bd8d420f1c9e55de19e0853",
        url="https://pypi.org/packages/ee/79/fa82a10cdf484b0e3153eeaa8c3ddad181e78d0d46eaa2236edee61305c4/jupyter_core-4.2.0-py2.py3-none-any.whl",
    )
    version(
        "4.1.1",
        sha256="33c9d6f61d271e8a8197cd5a2b1a1923bfe28d50eb947c1c30d51fe4f42e852d",
        url="https://pypi.org/packages/77/f0/fe465528064523f2d519b99a0b1591636a19011ab6dd4b02f03a2c6ad9a3/jupyter_core-4.1.1-py2.py3-none-any.whl",
    )
    version(
        "4.1.0",
        sha256="53c41ef5b4e62d452239aca4f4ce0147fac4033cde02a8b9a12ffded11eacad7",
        url="https://pypi.org/packages/87/cf/43a9c0d8ea808db7a4edd9157f8ba612e80c14be4ec5535ed2d300300628/jupyter_core-4.1.0-py2.py3-none-any.whl",
    )
    version(
        "4.0.6",
        sha256="985f2de832fef15a159b8d6ff14e4a90b7a10cb1f9beb102da710fd4cfcfd630",
        url="https://pypi.org/packages/37/45/182ca59bf976794b910c03138692e2f73785a6e475ea17553f9988332595/jupyter_core-4.0.6-py2.py3-none-any.whl",
    )
    version(
        "4.0.5",
        sha256="dac2033109158e90886e9a907d7ed5504aace96140f9ac798229cc375f3bbd17",
        url="https://pypi.org/packages/c8/fd/ce7a1dc81cbae811ca75bb3bcd91a7268401dee65f0cf86524b39205a332/jupyter_core-4.0.5-py2.py3-none-any.whl",
    )
    version(
        "4.0.4",
        sha256="672eabd762be76332f367b694462c3f49376fc2b7f47471daa21bb93b66002f7",
        url="https://pypi.org/packages/fa/35/a080617e7b7aaacbe859d0a93532b22f13ef0ab91b6be32079f89b4cf282/jupyter_core-4.0.4-py2.py3-none-any.whl",
    )
    version(
        "4.0.3",
        sha256="53c9b14e283625a24f6dc4f3cd38d5424a1593316f37432984f87c53822a260d",
        url="https://pypi.org/packages/e2/95/794da9ef8200e9302e747d5cec94eb0ffe30ecbe9dc3563d9ac1cffeaee9/jupyter_core-4.0.3-py2.py3-none-any.whl",
    )
    version(
        "4.0.2",
        sha256="881ef7e96d28a1fa1ebd72d27edb8d6324b279313de3e2729ebe1f2a4a0bc6b4",
        url="https://pypi.org/packages/86/7a/a6ab40c0b6ce81cc16be090082eeb0a2f7e5b0d83d309375f0e8405443cd/jupyter_core-4.0.2-py2.py3-none-any.whl",
    )
    version(
        "4.0.1",
        sha256="e3d1f13da845e88ed0fbc69da11d4090a762a95f43fb23cfc38e1a88c737dd2a",
        url="https://pypi.org/packages/1c/9a/fa1c65053b88bfded751e9ee9dc191e6a5112523fcdf6e6968681149a015/jupyter_core-4.0.1-py2.py3-none-any.whl",
    )
    version(
        "4.0.0",
        sha256="e9a60713cde81db888a5714f4f208be1b4e013c8adeb94e4f931df7a5914211a",
        url="https://pypi.org/packages/1f/6d/696c26f03bf64b402bd9f22884d6c5f59c87394f30a80bd1344be22128fb/jupyter_core-4.0.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@5.0.0:")
        depends_on("python@3.7:", when="@4.10:5.0.0-rc2")
        depends_on("py-platformdirs@2.5:", when="@5.1:")
        depends_on("py-pywin32@300:", when="@5.3: platform=windows")
        depends_on("py-pywin32", when="@4.6:5.2 platform=windows")
        depends_on("py-traitlets@5.3:5.3.0.0,5.4:", when="@5.1:")
        depends_on("py-traitlets", when="@4.1:5.0")

    # additional pywin32>=300 dependency for windows

    # Historical dependencies
