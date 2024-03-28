# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyParseType(PythonPackage):
    """parse_type extends the parse module (opposite of string.format())."""

    homepage = "https://github.com/jenisys/parse_type"
    pypi = "parse-type/parse_type-0.6.0.tar.gz"

    license("MIT")

    version(
        "0.6.0",
        sha256="c148e88436bd54dab16484108e882be3367f44952c649c9cd6b82a7370b650cb",
        url="https://pypi.org/packages/48/05/c7887ecb0adaab604bb4f7ced908ce0120b20abe588823dfca173ed407ab/parse_type-0.6.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-parse@1.18:", when="@0.6:")
        depends_on("py-six@1.11:", when="@0.4.2:0.6.0")
