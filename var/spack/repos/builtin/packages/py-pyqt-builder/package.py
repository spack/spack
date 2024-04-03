# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyqtBuilder(PythonPackage):
    """The PEP 517 compliant PyQt build system."""

    homepage = "https://www.riverbankcomputing.com/hg/PyQt-builder/"
    pypi = "PyQt-builder/PyQt-builder-1.12.2.tar.gz"

    license("GPL-2.0-or-later")

    version(
        "1.15.1",
        sha256="e15b8fdf47380636a1016e735435214720d7c18569f7f3a028b7d2982f872946",
        url="https://pypi.org/packages/44/f9/d836feeda500b2aeab4d95dda2d1c41d7b6a5e3e15a80ed3eb72096d9236/PyQt_builder-1.15.1-py3-none-any.whl",
    )
    version(
        "1.12.2",
        sha256="48f754394d235307201ec2b5355934858741201af09433ff543ca40ae57b7865",
        url="https://pypi.org/packages/e4/55/db354bd9dfa613c8f8f6ecb81617caefdfb3e77befba098f8e14ed95e385/PyQt_builder-1.12.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@1.13:")
        depends_on("py-packaging")
        depends_on("py-sip@6.7:", when="@1.14:")
        depends_on("py-sip@6.3:", when="@1.12:1.13")
