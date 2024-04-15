# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyResolvelib(PythonPackage):
    """Resolve abstract dependencies into concrete ones."""

    homepage = "https://github.com/sarugaku/resolvelib"
    pypi = "resolvelib/resolvelib-1.0.1.tar.gz"

    license("ISC")

    version(
        "1.0.1",
        sha256="d2da45d1a8dfee81bdd591647783e340ef3bcb104b54c383f70d422ef5cc7dbf",
        url="https://pypi.org/packages/d2/fc/e9ccf0521607bcd244aa0b3fbd574f71b65e9ce6a112c83af988bbbe2e23/resolvelib-1.0.1-py2.py3-none-any.whl",
    )
