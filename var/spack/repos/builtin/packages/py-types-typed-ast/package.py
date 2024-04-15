# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypesTypedAst(PythonPackage):
    """Typing stubs for typed-ast."""

    homepage = "https://github.com/python/typeshed"
    pypi = "types-typed-ast/types-typed-ast-1.5.8.3.tar.gz"

    version(
        "1.5.8.7",
        sha256="97bdd9b4228f96c6904a76e10a050305ddadb529bd35e4d8234711e09c41b543",
        url="https://pypi.org/packages/ca/c4/48fa43ca8d98503a6e826cf02681dbdd494058f3e3bb9bae38722507ca4e/types_typed_ast-1.5.8.7-py3-none-any.whl",
    )
    version(
        "1.5.8.3",
        sha256="d945082da658987e6f656e1b82373fe7f16acc1e5fe10bb1ebf2258e1b96a4bd",
        url="https://pypi.org/packages/2f/be/44b0b937b228fa2760d154a21069dd65151c8417ab2ddf499b1001084775/types_typed_ast-1.5.8.3-py3-none-any.whl",
    )
