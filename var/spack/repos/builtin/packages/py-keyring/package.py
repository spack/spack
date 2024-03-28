# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKeyring(PythonPackage):
    """The Python keyring library provides an easy way to access the system keyring
    service from python. It can be used in any application that needs safe password
    storage."""

    homepage = "https://github.com/jaraco/keyring"
    pypi = "keyring/keyring-23.0.1.tar.gz"

    license("MIT")

    version(
        "24.3.0",
        sha256="4446d35d636e6a10b8bce7caa66913dd9eca5fd222ca03a3d42c38608ac30836",
        url="https://pypi.org/packages/e3/e9/c51071308adc273ed612cd308a4b4360ffd291da40b7de2f47c9d6e3a978/keyring-24.3.0-py3-none-any.whl",
    )
    version(
        "23.13.1",
        sha256="771ed2a91909389ed6148631de678f82ddc73737d85a927f382a8a1b157898cd",
        url="https://pypi.org/packages/62/db/0e9a09b2b95986dcd73ac78be6ed2bd73ebe8bac65cba7add5b83eb9d899/keyring-23.13.1-py3-none-any.whl",
    )
    version(
        "23.9.1",
        sha256="3565b9e4ea004c96e158d2d332a49f466733d565bb24157a60fd2e49f41a0fd1",
        url="https://pypi.org/packages/fd/4e/eeaa2a3609cb0074a3cdd910f625adeec95aa1c1b6039816b18f5f7ca3fe/keyring-23.9.1-py3-none-any.whl",
    )
    version(
        "23.5.0",
        sha256="b0d28928ac3ec8e42ef4cc227822647a19f1d544f21f96457965dc01cf555261",
        url="https://pypi.org/packages/0d/bb/8e715dbb1886e6d7e4c6a7024c11a7e137559cd85366f25c67c2bdb311c3/keyring-23.5.0-py3-none-any.whl",
    )
    version(
        "23.2.1",
        sha256="bd2145a237ed70c8ce72978b497619ddfcae640b6dcf494402d5143e37755c6e",
        url="https://pypi.org/packages/58/b7/cc5a5321a6119e23ee85745ba204a67d646835e8882ba36eece32ee2b4e1/keyring-23.2.1-py3-none-any.whl",
    )
    version(
        "23.2.0",
        sha256="66a08700421ed0aaf317c6bf6543f7345f9ab9e7bed6e0ee072f7f6fcddbab75",
        url="https://pypi.org/packages/7a/18/bfa210920b2602114f804d72cd234cfd3f82ae213e0e4bb79b06561792d6/keyring-23.2.0-py3-none-any.whl",
    )
    version(
        "23.1.0",
        sha256="b32397fd7e7063f8dd74a26db910c9862fc2109285fa16e3b5208bcb42a3e579",
        url="https://pypi.org/packages/b5/00/d4ee8383decb2d3dd273a7d62027240e888fddf671ac4398adddd28e8717/keyring-23.1.0-py3-none-any.whl",
    )
    version(
        "23.0.1",
        sha256="8f607d7d1cc502c43a932a275a56fe47db50271904513a379d39df1af277ac48",
        url="https://pypi.org/packages/26/f9/41230ac47f738f1ba66676dc8d3b30ca5b1f9eb0230fc204bcd9836c4ae9/keyring-23.0.1-py3-none-any.whl",
    )
    version(
        "21.7.0",
        sha256="4c41ce4f6d1ee91d589a346699ef5a94ba3429603ac8f700cc0097644cdd6748",
        url="https://pypi.org/packages/e2/23/c15f403d1993a003a711a37318bbe66096c0802b265047919d5c14a4d693/keyring-21.7.0-py3-none-any.whl",
    )
    version(
        "20.0.1",
        sha256="c674f032424b4bffc62abeac5523ec49cc84aed07a480c3233e0baf618efc15c",
        url="https://pypi.org/packages/f1/07/0afb82d449d210a332d126978634470abdd0c754128a9ead8bbe78eb1b43/keyring-20.0.1-py2.py3-none-any.whl",
    )
    version(
        "18.0.1",
        sha256="7b29ebfcf8678c4da531b2478a912eea01e80007e5ddca9ee0c7038cb3489ec6",
        url="https://pypi.org/packages/cb/97/351c4839d78c518d8784822ec6f48f601de5cf47ab21242c0a6e5da888cc/keyring-18.0.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-entrypoints", when="@11.1:19.2")
        depends_on("py-importlib-metadata@4.11.4:", when="@23.10: ^python@:3.11")
        depends_on("py-importlib-metadata@3.6:", when="@23.6:23.9 ^python@:3.9")
        depends_on("py-importlib-metadata@3.6:", when="@22.4:23.5")
        depends_on("py-importlib-resources", when="@23.13: ^python@:3.8")
        depends_on("py-jaraco-classes", when="@23.9:")
        depends_on("py-jeepney@0.4.2:", when="@21.1: platform=linux")
        depends_on("py-pywin32-ctypes@0.2:", when="@23.12: platform=windows")
        depends_on("py-pywin32-ctypes@:0.0,0.1.2:", when="@10.4:23.11 platform=windows")
        depends_on("py-secretstorage@3.2:", when="@21.5: platform=linux")
        depends_on("py-secretstorage", when="@10:12.0.1,12.1:21.0 platform=linux")

    # TODO: additional dependency on pywin32-ctypes required for Windows

    # Historical dependencies
