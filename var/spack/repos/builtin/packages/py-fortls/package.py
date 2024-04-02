# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFortls(PythonPackage):
    """A Language Server for Fortran providing code completion, diagnostics, hovering and more."""

    homepage = "https://fortls.fortran-lang.org"
    pypi = "fortls/fortls-2.13.0.tar.gz"

    maintainers("RMeli")

    license("MIT")

    version(
        "2.13.0",
        sha256="85b42da62eba3f2048d740756ce944196bb36f867e0463f7917c4aa744aec34a",
        url="https://pypi.org/packages/ac/ea/74e100561654d9589fd70fe0b87b5b53b894a34a0549235f9f99a8702e90/fortls-2.13.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:")
        depends_on("py-importlib-metadata", when="^python@:3.7")
        depends_on("py-json5", when="@2.8:")
        depends_on("py-packaging")
        depends_on("py-typing-extensions", when="^python@:3.7")
