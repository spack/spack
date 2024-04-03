# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyStevedore(PythonPackage):
    """Manage Dynamic Plugins for Python Applications."""

    homepage = "https://docs.openstack.org/stevedore/latest/"
    pypi = "stevedore/stevedore-1.28.0.tar.gz"

    license("Apache-2.0")

    version(
        "4.0.0",
        sha256="87e4d27fe96d0d7e4fc24f0cbe3463baae4ec51e81d95fbe60d2474636e0c7d8",
        url="https://pypi.org/packages/d5/f7/7593812b0687e8aaf01b10f7f07bf59e5a6bbfcd9d657cefdeb48a72cd06/stevedore-4.0.0-py3-none-any.whl",
    )
    version(
        "3.5.0",
        sha256="a547de73308fd7e90075bb4d301405bebf705292fa90a90fc3bcf9133f58616c",
        url="https://pypi.org/packages/7a/bc/fcce9e50da73ea23af6d236e05e15db8a02da1099a5e0a479451bcea3833/stevedore-3.5.0-py3-none-any.whl",
    )
    version(
        "1.28.0",
        sha256="e3d96b2c4e882ec0c1ff95eaebf7b575a779fd0ccb4c741b9832bed410d58b3d",
        url="https://pypi.org/packages/17/6b/3b7d6d08b2ab3e5ef09e01c9f7b3b590ee135f289bb94553419e40922c25/stevedore-1.28.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@4:")
        depends_on("py-importlib-metadata@1.7:", when="@3 ^python@:3.7")
        depends_on("py-pbr@2:2.0,3:", when="@1.22:")
        depends_on("py-six@1.10:", when="@1.28:1")
