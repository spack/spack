# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPicmistandard(PythonPackage):
    """Standard input format for Particle-In-Cell codes"""

    homepage = "https://picmi-standard.github.io"
    git = "https://github.com/picmi-standard/picmi.git"
    pypi = "picmistandard/picmistandard-0.26.0.tar.gz"

    maintainers("ax3l", "dpgrote", "RemiLehe")

    version(
        "0.26.0",
        sha256="57607ca59110bb1e24a7998704b60e2a6af0a5171fd04595b582299803edd637",
        url="https://pypi.org/packages/9b/fd/65ea722c585eef271de7abb985cdce890393516dd5d0803f60a3f0e404e8/picmistandard-0.26.0-py3-none-any.whl",
    )
    version(
        "0.25.0",
        sha256="a69dd59459a732e7cd71a80a15de921560271ec23baac4f5d46014f4aac3d57d",
        url="https://pypi.org/packages/30/a9/fbd090129001eafca0847de4a00ad66b7da88db903499c68f6f420428553/picmistandard-0.25.0-py3-none-any.whl",
    )
    version(
        "0.24.0",
        sha256="3cd72f743cea7284d489e9282476e49b0f6e32c732de8eeeaf81a02e6e7f750b",
        url="https://pypi.org/packages/57/6c/07c87514e6b5ebea3ff4600831296f1ba1ae9c059c1b50f65150dce0086d/picmistandard-0.24.0-py3-none-any.whl",
    )
    version(
        "0.23.2",
        sha256="b3e34d2a39caaca0533775962538fcec8404cb5dfebb0058b99df641d74697da",
        url="https://pypi.org/packages/f9/89/eb52cf7a02154d79a475789b255071424cabde9e442c832c0f941c03ce5a/picmistandard-0.23.2-py3-none-any.whl",
    )
    version(
        "0.23.1",
        sha256="492e47e4085b9949d67fab3765a1383eb87b5c63a519ba935b3c7ac1183f7c72",
        url="https://pypi.org/packages/ac/0e/b9408e491f8c2662150eac7498001b412e1c11758d7fdc85ab529f25eeeb/picmistandard-0.23.1-py3-none-any.whl",
    )
    version(
        "0.0.22",
        sha256="2b4b4a360161f9af02cdaf424b14ab41b6c117344b5b6167b28b36a564846ff9",
        url="https://pypi.org/packages/32/dc/5c952c407dc8706af9a50e68659e1ee379f244a953bf3268755eb7fb620b/picmistandard-0.0.22-py3-none-any.whl",
    )
    version(
        "0.0.21",
        sha256="0109f191fcc7e80d575f8a1e6fc7bcb55332240c27865d62176741a079a54385",
        url="https://pypi.org/packages/24/20/54d5a57ea0fbd8a98cfd742044447923fe61272e507343f9640748a2bedd/picmistandard-0.0.21-py3-none-any.whl",
    )
    version(
        "0.0.20",
        sha256="18b30e06815d2eb350d1a71c02505eba47aa9e67224db7b03f14f3d9c70bea5c",
        url="https://pypi.org/packages/75/42/2184fb2643dcf1da150f06a79a929e8669e321e01709811553d357b45bdd/picmistandard-0.0.20-py3-none-any.whl",
    )
    version(
        "0.0.19",
        sha256="19e3a7a7d33a7effa8f11f941702d965f1da1874a02aedef25df3b66f045d611",
        url="https://pypi.org/packages/00/af/b79b99a5a1096beda7753c6f0b88cccc936588ada4d85c18c91c016d5437/picmistandard-0.0.19-py3-none-any.whl",
    )
    version(
        "0.0.18",
        sha256="7095927820ac6feef6789b17251f78ced4fbfc1fe186a258244d864776e132ae",
        url="https://pypi.org/packages/84/7c/bcc1a7227740e40308e6f0a8d8418db7b58323f972ebfb95d551e8a1e748/picmistandard-0.0.18-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-numpy@1.15.0:1", when="@0.0.15:")
        depends_on("py-scipy@1.5.0:", when="@0.0.15:")
