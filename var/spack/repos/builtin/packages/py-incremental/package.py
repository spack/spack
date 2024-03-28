# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIncremental(PythonPackage):
    """A small library that versions your Python projects."""

    homepage = "https://github.com/twisted/incremental"
    pypi = "incremental/incremental-21.3.0.tar.gz"

    license("MIT")

    version(
        "21.3.0",
        sha256="92014aebc6a20b78a8084cdd5645eeaa7f74b8933f70fa3ada2cfbd1e3b54321",
        url="https://pypi.org/packages/99/3b/4f80dd10cb716f3a9e22ae88f026d25c47cc3fdf82c2747f3d59c98e4ff1/incremental-21.3.0-py2.py3-none-any.whl",
    )
