# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVirtualenv(PythonPackage):
    """virtualenv is a tool to create isolated Python environments."""

    homepage = "https://virtualenv.pypa.io/"
    pypi = "virtualenv/virtualenv-16.7.6.tar.gz"
    git = "https://github.com/pypa/virtualenv.git"

    license("MIT")

    version(
        "20.24.5",
        sha256="b80039f280f4919c77b30f1c23294ae357c4c8701042086e3fc005963e4e537b",
        url="https://pypi.org/packages/4e/8b/f0d3a468c0186c603217a6656ea4f49259630e8ed99558501d92f6ff7dc3/virtualenv-20.24.5-py3-none-any.whl",
    )
    version(
        "20.22.0",
        sha256="48fd3b907b5149c5aab7c23d9790bea4cac6bc6b150af8635febc4cfeab1275a",
        url="https://pypi.org/packages/b9/dc/44f55e57b8c106391987b17fe17db0ef3cc6364a935d1691b89df0e149a7/virtualenv-20.22.0-py3-none-any.whl",
    )
    version(
        "20.17.1",
        sha256="ce3b1684d6e1a20a3e5ed36795a97dfc6af29bc3970ca8dab93e11ac6094b3c4",
        url="https://pypi.org/packages/18/a2/7931d40ecb02b5236a34ac53770f2f6931e3082b7a7dafe915d892d749d6/virtualenv-20.17.1-py3-none-any.whl",
    )
    version(
        "20.16.4",
        sha256="035ed57acce4ac35c82c9d8802202b0e71adac011a511ff650cbcf9635006a22",
        url="https://pypi.org/packages/4f/8c/2f44bb00c152f24d980c91b95c0b0f38f814eb5b7a7da102467d23749ee3/virtualenv-20.16.4-py3-none-any.whl",
    )
    version(
        "20.10.0",
        sha256="4b02e52a624336eece99c96e3ab7111f469c24ba226a53ec474e8e787b365814",
        url="https://pypi.org/packages/ac/8a/05e8d8a3ac88a3c4ebec1fe2b1b4730e6e6ebdddb52cfd6cea6803de4624/virtualenv-20.10.0-py2.py3-none-any.whl",
    )
    version(
        "16.7.6",
        sha256="3e3597e89c73df9313f5566e8fc582bd7037938d15b05329c232ec57a11a7ad5",
        url="https://pypi.org/packages/89/66/786e0d6f61bd0612f431e19b016d1ae46f1cb8d21a80352cc6774ec876e3/virtualenv-16.7.6-py2.py3-none-any.whl",
    )
    version(
        "16.4.1",
        sha256="dffd40d19ab0168c02cf936de59590a3c0f2c8c4a36f363fcf3dae18728dc94e",
        url="https://pypi.org/packages/88/b6/9f2e13a71e5a7cd458dcf4f24540a4bd39206cc6290e8393a48d8b95c11e/virtualenv-16.4.1-py2.py3-none-any.whl",
    )
    version(
        "16.0.0",
        sha256="2ce32cd126117ce2c539f0134eb89de91a8413a29baac49cbab3eb50e2026669",
        url="https://pypi.org/packages/b6/30/96a02b2287098b23b875bc8c2f58071c35d2efe84f747b64d523721dc2b5/virtualenv-16.0.0-py2.py3-none-any.whl",
    )
    version(
        "15.1.0",
        sha256="39d88b533b422825d644087a21e78c45cf5af0ef7a99a1fc9fbb7b481e5c85b0",
        url="https://pypi.org/packages/6f/86/3dc328ee7b1a6419ebfac7896d882fba83c48e3561d22ddddf38294d3e83/virtualenv-15.1.0-py2.py3-none-any.whl",
    )
    version(
        "15.0.1",
        sha256="13ce1079910a6bc60e2ce1d79813a99f30b2fd1e571427fcde1fabb0ff4c436c",
        url="https://pypi.org/packages/bb/83/1aa921ab8c7d017e4098582acbc422a30485f820290577b361c8fc407d53/virtualenv-15.0.1-py2.py3-none-any.whl",
    )
    version(
        "13.0.1",
        sha256="da85f7ea539cfec9437f4d87d12f95d34d92a6d30485e85a4bc434bcdff7c6c3",
        url="https://pypi.org/packages/3f/21/8503e2592183d552c6e47fc431b3976c7b53256b1d1c50eb1f12ada2238c/virtualenv-13.0.1-py2.py3-none-any.whl",
    )
    version(
        "1.11.6",
        sha256="a8e07085d85c637c463ae23dc0911f32c871eddef69765ff9fa26cac9f2c5053",
        url="https://pypi.org/packages/c6/e3/f1eaf5a62fb7df7d98f39e7f45521f562bed2b6ab405a81d678e844a4ef2/virtualenv-1.11.6-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@20.18:")
        depends_on("py-backports-entry-points-selectable@1.0.4:", when="@20.5:20.10")
        depends_on("py-distlib@0.3.7:", when="@20.24.2:")
        depends_on("py-distlib@0.3.6:", when="@20.16.6:20.24.1")
        depends_on("py-distlib@0.3.5:", when="@20.16.3:20.16.5")
        depends_on("py-distlib@0.3.1:", when="@20.0.26:20.16.2")
        depends_on("py-filelock@3.12.2:", when="@20.24.2:")
        depends_on("py-filelock@3.11:", when="@20.22:20.23.0")
        depends_on("py-filelock@3.4.1:", when="@20.16.3:20.21")
        depends_on("py-filelock@3.2:", when="@20.9:20.16.2")
        depends_on("py-importlib-metadata@6.6:", when="@20.23.1: ^python@:3.7")
        depends_on("py-importlib-metadata@6.4.1:", when="@20.22:20.23.0 ^python@:3.7")
        depends_on("py-importlib-metadata@4.8.3:", when="@20.16.3:20.21 ^python@:3.7")
        depends_on("py-importlib-metadata@0.12:", when="@20.2.1:20.16.2 ^python@:3.7")
        depends_on("py-importlib-resources@5.4:", when="@20.16.3:20.17 ^python@:3.6")
        depends_on("py-importlib-resources@1:", when="@20.0.22:20.16.2 ^python@:3.6")
        depends_on("py-platformdirs@3.9.1:3", when="@20.24.2:20.24.6")
        depends_on("py-platformdirs@3.2:3", when="@20.22:20.23.0")
        depends_on("py-platformdirs@2.4:2", when="@20.16.3:20.18")
        depends_on("py-platformdirs@2.0.0:2", when="@20.5:20.16.2")
        depends_on("py-six@1.9:", when="@20.0.4:20.15")

    # Historical dependencies

    skip_modules = ["virtualenv.discovery.windows"]
