# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCylcRose(PythonPackage):
    """A Cylc plugin providing support for the Rose rose-suite.conf file."""

    homepage = "https://cylc.github.io/cylc-doc/latest/html/plugins/cylc-rose.html"
    pypi = "cylc-rose/cylc-rose-1.3.0.tar.gz"

    maintainers("LydDeb")

    license("GPL-3.0-only")

    version(
        "1.3.0",
        sha256="34319cefea4f039de9babc72e79788ca7b38a13f7df52bf26ab862f07005c205",
        url="https://pypi.org/packages/bd/16/9d591c837df9e0321d678fd65206a01dd74f15afc43e078b2b7d7ad90c3a/cylc_rose-1.3.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@1:")
        depends_on("py-cylc-flow@8.2:", when="@1.3:")
        depends_on("py-jinja2", when="@1:")
        depends_on("py-metomi-isodatetime", when="@1:")
        depends_on("py-metomi-rose@2.1", when="@1.3:1.3.1")
