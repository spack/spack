# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PySnoop(PythonPackage):
    """snoop is a powerful set of Python debugging tools. It's primarily meant
    to be a more featureful and refined version of PySnooper. It also includes
    its own version of icecream and some other nifty stuff."""

    pypi = "snoop/snoop-0.4.3.tar.gz"

    license("MIT", checked_by="jmlapre")

    version(
        "0.4.3",
        sha256="b7418581889ff78b29d9dc5ad4625c4c475c74755fb5cba82c693c6e32afadc0",
        url="https://pypi.org/packages/10/b4/5eb395a7c44f382f42cc4ce2d544223c0506e06c61534f45a2188b8fdf13/snoop-0.4.3-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-asttokens", when="@0.4.1:")
        depends_on("py-cheap-repr@0.4:", when="@0.4.1:")
        depends_on("py-executing", when="@0.4.1:")
        depends_on("py-pygments", when="@0.4.1:")
        depends_on("py-six", when="@0.4.1:")
