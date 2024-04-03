# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypesUrllib3(PythonPackage):
    """Typing stubs for urllib3."""

    homepage = "https://github.com/python/typeshed"
    pypi = "types-urllib3/types-urllib3-1.26.24.tar.gz"

    version(
        "1.26.25.14",
        sha256="9683bbb7fb72e32bfe9d2be6e04875fbe1b3eeec3cbb4ea231435aa7fd6b4f0e",
        url="https://pypi.org/packages/11/7b/3fc711b2efea5e85a7a0bbfe269ea944aa767bbba5ec52f9ee45d362ccf3/types_urllib3-1.26.25.14-py3-none-any.whl",
    )
    version(
        "1.26.24",
        sha256="cf7918503d02d3576e503bbfb419b0e047c4617653bba09624756ab7175e15c9",
        url="https://pypi.org/packages/34/ed/9c4981c4d86bbd255a664fd19fe83a287766001300f5b8384cc2a5e61cb8/types_urllib3-1.26.24-py3-none-any.whl",
    )
