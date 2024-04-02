# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOverrides(PythonPackage):
    """A decorator to automatically detect mismatch when overriding a method."""

    homepage = "https://github.com/mkorpela/overrides"
    pypi = "overrides/overrides-7.3.1.tar.gz"

    license("Apache-2.0")

    version(
        "7.3.1",
        sha256="6187d8710a935d09b0bcef8238301d6ee2569d2ac1ae0ec39a8c7924e27f58ca",
        url="https://pypi.org/packages/7f/36/3fef66c2bf1f66f35538a6703aca0447114b1873913c403f0ea589721aae/overrides-7.3.1-py3-none-any.whl",
    )
