# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPreCommit(PythonPackage):
    """A framework for managing and maintaining multi-language pre-commit
    hooks."""

    homepage = "https://github.com/pre-commit/pre-commit"
    pypi = "pre_commit/pre_commit-1.20.0.tar.gz"

    license("MIT")

    version(
        "3.6.0",
        sha256="c255039ef399049a5544b6ce13d135caba8f2c28c3b4033277a788f434308376",
        url="https://pypi.org/packages/e2/e3/54cd906d377e1766299df14710ded125e195d5c685c8f1bafecec073e9c6/pre_commit-3.6.0-py2.py3-none-any.whl",
    )
    version(
        "3.5.0",
        sha256="841dc9aef25daba9a0238cd27984041fa0467b4199fc4852e27950664919f660",
        url="https://pypi.org/packages/6c/75/526915fedf462e05eeb1c75ceaf7e3f9cde7b5ce6f62740fe5f7f19a0050/pre_commit-3.5.0-py2.py3-none-any.whl",
    )
    version(
        "3.3.3",
        sha256="10badb65d6a38caff29703362271d7dca483d01da88f9d7e05d0b97171c136cb",
        url="https://pypi.org/packages/e3/b7/1d145c985d8be9729672a45b8b8113030ad60dff45dec592efc4e5f5897a/pre_commit-3.3.3-py2.py3-none-any.whl",
    )
    version(
        "2.20.0",
        sha256="51a5ba7c480ae8072ecdb6933df22d2f812dc897d5fe848778116129a681aac7",
        url="https://pypi.org/packages/b2/6c/9ccb5213a3d9fd3f8c0fd69d207951901eaef86b7a1a69bcc478364d3072/pre_commit-2.20.0-py2.py3-none-any.whl",
    )
    version(
        "2.17.0",
        sha256="725fa7459782d7bec5ead072810e47351de01709be838c2ce1726b9591dad616",
        url="https://pypi.org/packages/d6/a0/9c06353771c8dae6db437dd513a885eccdb1566cb332569130484eddf4e7/pre_commit-2.17.0-py2.py3-none-any.whl",
    )
    version(
        "2.10.1",
        sha256="16212d1fde2bed88159287da88ff03796863854b04dc9f838a55979325a3d20e",
        url="https://pypi.org/packages/7d/ce/382156bfb1919168354dd6b441b9dd553e264fa7190073a0af3ee52b001e/pre_commit-2.10.1-py2.py3-none-any.whl",
    )
    version(
        "1.20.0",
        sha256="c2e4810d2d3102d354947907514a78c5d30424d299dc0fe48f5aa049826e9b50",
        url="https://pypi.org/packages/89/97/fe584f47dc43332ac254ed3940d2a3401877be73e3150a557641c9f812a6/pre_commit-1.20.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.9:", when="@3.6:")
        depends_on("python@3.8:", when="@3:3.5")
        depends_on("python@3.7:", when="@2.18:2")
        depends_on("py-aspy-yaml", when="@:2.0")
        depends_on("py-cfgv@2:", when="@1.17:")
        depends_on("py-identify@1:")
        depends_on("py-importlib-metadata", when="@1.19:2 ^python@:3.7")
        depends_on("py-importlib-resources@:5.2", when="@2.16:2.17 ^python@:3.6")
        depends_on("py-importlib-resources", when="@:2.15 ^python@:3.6")
        depends_on("py-nodeenv@0.11.1:")
        depends_on("py-pyyaml@5.1:", when="@2.1:")
        depends_on("py-pyyaml", when="@:2.0")
        depends_on("py-six", when="@:1")
        depends_on("py-toml", when="@:2.20")
        depends_on("py-virtualenv@20.10:", when="@2.21:")
        depends_on("py-virtualenv@20.0.8:", when="@2.4:2.20")
        depends_on("py-virtualenv@15.2:", when="@:2.3")

    # Historical dependencies
