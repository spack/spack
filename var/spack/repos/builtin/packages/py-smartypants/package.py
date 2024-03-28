# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySmartypants(PythonPackage):
    """smartypants is a Python fork of SmartyPants."""

    homepage = "https://github.com/leohemsted/smartypants.py"

    # PyPI only has the wheel
    url = "https://github.com/leohemsted/smartypants.py/archive/refs/tags/v2.0.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "2.0.1",
        sha256="8db97f7cbdf08d15b158a86037cd9e116b4cf37703d24e0419a0d64ca5808f0d",
        url="https://pypi.org/packages/da/ed/1da76d11aa858ee23dac5b52d9ac2db7df02b89f7679d5d8970bcd44b59c/smartypants-2.0.1-py2.py3-none-any.whl",
    )
