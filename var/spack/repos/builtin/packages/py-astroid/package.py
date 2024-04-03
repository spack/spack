# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAstroid(PythonPackage):
    """A common base representation of python source code for pylint
    and other projects."""

    homepage = "https://github.com/PyCQA/astroid"
    pypi = "astroid/astroid-2.8.3.tar.gz"

    license("LGPL-2.1-or-later")

    version(
        "2.14.2",
        sha256="0e0e3709d64fbffd3037e4ff403580550f14471fd3eaae9fa11cc9a5c7901153",
        url="https://pypi.org/packages/ae/40/d6fbafb01a3da14289c7cc8ff82a0513ccd82a49219ffa84c67a46b1b712/astroid-2.14.2-py3-none-any.whl",
    )
    version(
        "2.12.10",
        sha256="997e0c735df60d4a4caff27080a3afc51f9bdd693d3572a4a0b7090b645c36c5",
        url="https://pypi.org/packages/68/48/7f3de2f4f94f0b18afe5bc1b587a23b4f9a173909db4eff9cc7d92b8d3cc/astroid-2.12.10-py3-none-any.whl",
    )
    version(
        "2.12.7",
        sha256="9b408d5d540387a74ca5405a5197aa24fbf9178b4019b16b3e532fbdf0e467cc",
        url="https://pypi.org/packages/bd/9a/6ed1fe23ae26fe6f0a8064f96ab7b41c517885076253a43464acfe6f497e/astroid-2.12.7-py3-none-any.whl",
    )
    version(
        "2.11.6",
        sha256="ba33a82a9a9c06a5ceed98180c5aab16e29c285b828d94696bf32d6015ea82a9",
        url="https://pypi.org/packages/b6/38/1b2188bea6b5346ea2f97f063c99fdadb36707a7b3a95ff4fe73e242c33c/astroid-2.11.6-py3-none-any.whl",
    )
    version(
        "2.11.5",
        sha256="14ffbb4f6aa2cf474a0834014005487f7ecd8924996083ab411e7fa0b508ce0b",
        url="https://pypi.org/packages/94/58/6f1bbfd88b6ba5271b4a9be99cb15cb2fe369794ba410390f0d672c6ad39/astroid-2.11.5-py3-none-any.whl",
    )
    version(
        "2.11.4",
        sha256="da0632b7c046d8361dfe1b1abb2e085a38624961fabe2997565a9c06c1be9d9a",
        url="https://pypi.org/packages/24/f1/d3b7d72cae86abb75a28b2ae7be0668452753507e8156c9955b244fbc795/astroid-2.11.4-py3-none-any.whl",
    )
    version(
        "2.8.3",
        sha256="f9d66e3a4a0e5b52819b2ff41ac2b179df9d180697db71c92beb33a60c661794",
        url="https://pypi.org/packages/c1/a5/be9c96e816a9159ef2e54ef030158360e8539da2bd9ce8a82208d2a0a640/astroid-2.8.3-py3-none-any.whl",
    )
    version(
        "2.7.3",
        sha256="dc1e8b28427d6bbef6b8842b18765ab58f558c42bb80540bd7648c98412af25e",
        url="https://pypi.org/packages/2f/2b/46d2b492831ea7a637b88bef8e66aae0968edf57042d1f52073a531558ea/astroid-2.7.3-py3-none-any.whl",
    )
    version(
        "2.5.6",
        sha256="4db03ab5fc3340cf619dbc25e42c2cc3755154ce6009469766d7143d1fc2ee4e",
        url="https://pypi.org/packages/f8/82/a61df6c2d68f3ae3ad1afa0d2e5ba5cfb7386eb80cffb453def7c5757271/astroid-2.5.6-py3-none-any.whl",
    )
    version(
        "2.4.2",
        sha256="bc58d83eb610252fd8de6363e39d4f1d0619c894b0ed24603b881c02e64c7386",
        url="https://pypi.org/packages/24/a8/5133f51967fb21e46ee50831c3f5dda49e976b7f915408d670b1603d41d6/astroid-2.4.2-py3-none-any.whl",
    )
    version(
        "1.6.6",
        sha256="87de48a92e29cedf7210ffa853d11441e7ad94cb47bacd91b023499b51cbc756",
        url="https://pypi.org/packages/8b/29/0f7ec6fbf28a158886b7de49aee3a77a8a47a7e24c60e9fd6ec98ee2ec02/astroid-1.6.6-py2.py3-none-any.whl",
    )
    version(
        "1.4.5",
        sha256="46cd033dddbc3dc602d64991949d43232cf08d53cd4c06cae224895d542d9358",
        url="https://pypi.org/packages/da/6b/bce6c46354d8bb59ad842f737084c176c636b7f94caf7aa5974d1c41ebbf/astroid-1.4.5-py2.py3-none-any.whl",
    )
    version(
        "1.4.4",
        sha256="5e09d952001bce3ad0f700f982f58658b5f2d1ae3761e60d7d2645fa7b19c0fc",
        url="https://pypi.org/packages/1e/d7/9622bc4593fc86738f47b78c87cf70388ed84cae3305306b17d08ff367d2/astroid-1.4.4-py2.py3-none-any.whl",
    )
    version(
        "1.4.3",
        sha256="c4ce2041da305960ee290e0d45482668dcbe7fb5047030636a0996b344ac978a",
        url="https://pypi.org/packages/4e/e4/692b43ca0228da68179925ef43fa531cdf67c78334bdb5790ed2718141f3/astroid-1.4.3-py2.py3-none-any.whl",
    )
    version(
        "1.4.2",
        sha256="34d3ca4e7369e15c5b9f76a441ede106c351d6d0f256cd6eb286b2bebeec0db3",
        url="https://pypi.org/packages/c9/a2/df818426ce8c437363c35fcb8d0b6570c765181793797cfd9d483fe99bdf/astroid-1.4.2-py2.py3-none-any.whl",
    )
    version(
        "1.4.1",
        sha256="3e369a37695390d1c5a4c292b84f3ce7673f5ac93a92f328522c42cb26fd20ef",
        url="https://pypi.org/packages/3a/5b/66057c670184eec8adffa2d9eda78ee4bbcf9c043acbd839c5f609365e89/astroid-1.4.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@2.12:2")
        depends_on("python@:3", when="@2.5.4:2.9.0")
        depends_on("py-lazy-object-proxy@1.4:", when="@2.5:2")
        depends_on("py-lazy-object-proxy@1.4", when="@2:2.4")
        depends_on("py-lazy-object-proxy", when="@1.6:1")
        depends_on("py-setuptools@20:", when="@2.6.3:2.11")
        depends_on("py-six@1.12:", when="@2:2.4")
        depends_on("py-six", when="@1.6:1")
        depends_on("py-typed-ast@1.4:", when="@2.8.5:2 ^python@:3.7")
        depends_on("py-typed-ast@1.4", when="@2:2.8.4 ^python@:3.7")
        depends_on("py-typing-extensions@4:", when="@2.13.3: ^python@:3.10")
        depends_on("py-typing-extensions@3.10:", when="@2.8:2.13.0 ^python@:3.9")
        depends_on("py-typing-extensions@3.7.4:", when="@2.5.7:2.7 ^python@:3.7")
        depends_on("py-wrapt@1.14.0:", when="@2.12.3:2 ^python@3.11:")
        depends_on("py-wrapt@1.11:", when="@2.12.3:2 ^python@:3.10")
        depends_on("py-wrapt@1.11:1.13", when="@2.8.3:2.10")
        depends_on("py-wrapt@1.11:1.12", when="@2.5:2.8.2")
        depends_on("py-wrapt@1.11:", when="@2:2.4,2.11:2.12.2")
        depends_on("py-wrapt", when="@1.6:1")

    # fixes symlink resolution, already included in 2: but not in 1.6.6

    # Dependencies taken from astroid/__pkginfo__.py
    # Starting with astroid 2.3.1, astroid's dependencies were restricted
    # to a given minor version, c.f. commit e1b4e11.
