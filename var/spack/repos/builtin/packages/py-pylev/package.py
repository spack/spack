# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPylev(PythonPackage):
    """A pure Python Levenshtein implementation that's not freaking GPL'd."""

    homepage = "http://github.com/toastdriven/pylev"
    pypi = "pylev/pylev-1.4.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "1.4.0",
        sha256="7b2e2aa7b00e05bb3f7650eb506fc89f474f70493271a35c242d9a92188ad3dd",
        url="https://pypi.org/packages/04/78/95cfe72991d22994f0ec5a3b742b31c95a28344d33e06b69406b68398a29/pylev-1.4.0-py2.py3-none-any.whl",
    )
