# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypesTypedAst(PythonPackage):
    """Typing stubs for typed-ast."""

    homepage = "https://github.com/python/typeshed"
    pypi = "types-typed-ast/types-typed-ast-1.5.8.3.tar.gz"

    version("1.5.8.3", sha256="3a62bc25168f8b44ce74e1114f9fbc2ee87d6e96e3880cbef39aad9522555b4e")

    depends_on("py-setuptools", type="build")
