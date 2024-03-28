# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypesSetuptools(PythonPackage):
    """Typing stubs for setuptools."""

    homepage = "https://github.com/python/typeshed"
    pypi = "types-setuptools/types-setuptools-65.5.0.3.tar.gz"

    version(
        "68.2.0.0",
        sha256="77edcc843e53f8fc83bb1a840684841f3dc804ec94562623bfa2ea70d5a2ba1b",
        url="https://pypi.org/packages/5c/5a/fbfbe3d1db90c59fb0240cf13a84953677b15874d00e80e773425447633c/types_setuptools-68.2.0.0-py3-none-any.whl",
    )
    version(
        "65.5.0.3",
        sha256="9254c32b0cc91c486548e7d7561243b5bd185402a383e93c6691e1b9bc8d86e2",
        url="https://pypi.org/packages/1e/07/77f506c72429f68756abc363b5f9e7fd4203a21f896c19a5c370cc274012/types_setuptools-65.5.0.3-py3-none-any.whl",
    )
