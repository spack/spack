# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDominate(PythonPackage):
    """Dominate is a Python library for creating and
    manipulating HTML documents using an elegant DOM API. It
    allows you to write HTML pages in pure Python very
    concisely, which eliminates the need to learn another
    template language, and lets you take advantage of the more
    powerful features of Python."""

    homepage = "https://github.com/Knio/dominate"
    pypi = "dominate/dominate-2.6.0.tar.gz"
    # license = "LGPL-3.0"

    license("LGPL-3.0-or-later")

    version(
        "2.6.0",
        sha256="84b5f71ed30021193cb0faa45d7776e1083f392cfe67a49f44e98cb2ed76c036",
        url="https://pypi.org/packages/ef/a8/4354f8122c39e35516a2708746d89db5e339c867abbd8e0179bccee4b7f9/dominate-2.6.0-py2.py3-none-any.whl",
    )
