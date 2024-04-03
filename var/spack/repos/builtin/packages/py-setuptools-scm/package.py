# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySetuptoolsScm(PythonPackage):
    """The blessed package to manage your versions by scm tags."""

    homepage = "https://github.com/pypa/setuptools_scm"
    pypi = "setuptools_scm/setuptools_scm-4.1.2.tar.gz"

    license("MIT")

    version(
        "7.1.0",
        sha256="73988b6d848709e2af142aa48c986ea29592bbcfca5375678064708205253d8e",
        url="https://pypi.org/packages/1d/66/8f42c941be949ef2b22fe905d850c794e7c170a526023612aad5f3a121ad/setuptools_scm-7.1.0-py3-none-any.whl",
    )
    version(
        "7.0.5",
        sha256="7930f720905e03ccd1e1d821db521bff7ec2ac9cf0ceb6552dd73d24a45d3b02",
        url="https://pypi.org/packages/01/ed/75a20e7b075e8ecb1f84e8debf833917905d8790b78008915bd68dddd5c4/setuptools_scm-7.0.5-py3-none-any.whl",
    )
    version(
        "7.0.3",
        sha256="7934c856b042199eb44e1523b46abb881726b7d61b3c9b41a756e4ffb4adf73b",
        url="https://pypi.org/packages/cb/50/a88ad10c10caba0a375123db0dc9ff31c075655eb844135f57691925298f/setuptools_scm-7.0.3-py3-none-any.whl",
    )
    version(
        "6.3.2",
        sha256="4c64444b1d49c4063ae60bfe1680f611c8b13833d556fd1d6050c0023162a119",
        url="https://pypi.org/packages/bc/bf/353180314d0e27929703faf240c244f25ae765e01f595a010cafb209ab51/setuptools_scm-6.3.2-py3-none-any.whl",
    )
    version(
        "6.0.1",
        sha256="c3bd5f701c8def44a5c0bfe8d407bef3f80342217ef3492b951f3777bd2d915c",
        url="https://pypi.org/packages/c4/d5/e50358c82026f44cd8810c8165002746cd3f8b78865f6bcf5d7f0fe4f652/setuptools_scm-6.0.1-py3-none-any.whl",
    )
    version(
        "5.0.2",
        sha256="bd5c4e37f74c103e117549f89aeb3c244488c4a6422df786d1a7d03257f16b34",
        url="https://pypi.org/packages/6a/18/23ad8654c5c8d91d1238b2d52882e50152473f2bd2db0da60215b51f401b/setuptools_scm-5.0.2-py2.py3-none-any.whl",
    )
    version(
        "4.1.2",
        sha256="69258e2eeba5f7ce1ed7a5f109519580fa3578250f8e4d6684859f86d1b15826",
        url="https://pypi.org/packages/ad/d3/e54f8b4cde0f6fb4f231629f570c1a33ded18515411dee6df6fe363d976f/setuptools_scm-4.1.2-py2.py3-none-any.whl",
    )
    version(
        "3.5.0",
        sha256="0d23db3d43e0a43eb7196bcf0eb8a4a2eb0561f621ed7ec44b2fdccfd907e38f",
        url="https://pypi.org/packages/4b/c1/118ec08816737cc46b4dd93b22f7a138fbfb14b53f4b4718fd9983e70a50/setuptools_scm-3.5.0-py2.py3-none-any.whl",
    )
    version(
        "3.3.3",
        sha256="1f11cb2eea431346d46589c2dafcafe2e7dc1c7b2c70bc4c3752d2048ad5c148",
        url="https://pypi.org/packages/1d/70/97966deebaeeda0b81d3cd63ba9f8ec929b838871ed17476de9d8159db3e/setuptools_scm-3.3.3-py2.py3-none-any.whl",
    )
    version(
        "3.1.0",
        sha256="cc6953d224a22f10e933fa2f55c95979317c55259016adcf93310ba2997febfa",
        url="https://pypi.org/packages/b2/d5/970632917c53a1fb2751f7da8b288d26546f2b113e4321674051fc9f81e4/setuptools_scm-3.1.0-py2.py3-none-any.whl",
    )
    version(
        "1.15.6",
        sha256="dac89650c7909d238965e163e10b736cbd3a72f28e2dd5c0fea6cf5e49e8562e",
        url="https://pypi.org/packages/54/66/00a0e93b02409454af83cfbd782887b5b131dd915af23d53c6651d7cc039/setuptools_scm-1.15.6-py2.py3-none-any.whl",
    )

    variant("toml", default=True, description="Build with TOML support")

    with default_args(type="run"):
        depends_on("python@3.7:", when="@7")
        depends_on("py-importlib-metadata", when="@7.0.1:7 ^python@:3.7")
        depends_on("py-packaging@20:", when="@6.3:")
        depends_on("py-setuptools@42:", when="@6.3:7+toml")
        depends_on("py-setuptools@45:", when="@6:6.2")
        depends_on("py-setuptools", when="@4:5,6.3:")
        depends_on("py-toml", when="@4:6.0,6.1.0.dev:6.1.0+toml")
        depends_on("py-tomli@1:", when="@7.1: ^python@:3.10")
        depends_on("py-tomli@1:", when="@6.3+toml")
        depends_on("py-tomli@1:", when="@6.2,6.3.1:7.0")
        depends_on("py-typing-extensions", when="@7,8.0.4:")

    # Basically a no-op in setuptools_scm 7+, toml support is always built
