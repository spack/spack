# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCookiecutter(PythonPackage):
    """A command-line utility that creates projects from cookiecutters
    (project templates).  E.g. Python package projects, jQuery plugin
    projects."""

    homepage = "https://cookiecutter.readthedocs.io/en/latest/"
    url = "https://github.com/audreyr/cookiecutter/archive/1.6.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "1.6.0",
        sha256="ed8f54a8fc79b6864020d773ce11539b5f08e4617f353de1f22d23226f6a0d36",
        url="https://pypi.org/packages/16/99/1ca3a75978270288354f419e9166666801cf7e7d8df984de44a7d5d8b8d0/cookiecutter-1.6.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-binaryornot@0.2:", when="@1.6:1.7.0")
        depends_on("py-click@5:", when="@1.6")
        depends_on("py-future@0.15.2:", when="@1.6:1.7.0")
        depends_on("py-jinja2@2.7:", when="@1.6:1.7.0")
        depends_on("py-jinja2-time", when="@1.6:1.7.0")
        depends_on("py-poyo", when="@1.6:1.7.0")
        depends_on("py-requests@2.18:", when="@1.6:1.7.0")
        depends_on("py-whichcraft@0.4:", when="@1.6:1.7.0")
