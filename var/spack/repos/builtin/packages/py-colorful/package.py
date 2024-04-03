# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyColorful(PythonPackage):
    """Terminal string styling done right, in Python."""

    homepage = "https://github.com/timofurrer/colorful"
    pypi = "colorful/colorful-0.5.4.tar.gz"

    license("MIT")

    version(
        "0.5.4",
        sha256="8d264b52a39aae4c0ba3e2a46afbaec81b0559a99be0d2cfe2aba4cf94531348",
        url="https://pypi.org/packages/b0/8e/e386e248266952d24d73ed734c2f5513f34d9557032618c8910e605dfaf6/colorful-0.5.4-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-colorama", when="platform=windows")
