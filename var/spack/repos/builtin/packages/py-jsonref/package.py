# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJsonref(PythonPackage):
    """An implementation of JSON Reference for Python"""

    homepage = "https://github.com/gazpachoking/jsonref"
    pypi = "jsonref/jsonref-0.2.tar.gz"

    license("MIT")

    version(
        "0.2",
        sha256="b1e82fa0b62e2c2796a13e5401fe51790b248f6d9bf9d7212a3e31a3501b291f",
        url="https://pypi.org/packages/07/92/f8e4ac824b14af77e613984e480fa818397c72d4141fc466decb26752749/jsonref-0.2-py3-none-any.whl",
    )
