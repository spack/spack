# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyem(PythonPackage):
    """Project-level Python virtual environment management tool.

    PyEM manages multiple virtual environments local to projects.
    It provides shortcuts to create, remove, switch between, and run
    commands against virtual environments created against
    various Python interpreters."""

    pypi = "pyem/pyem-2.1.0.tar.gz"

    license("ISC")

    version(
        "2.1.0",
        sha256="1970b55569d21e80734c428d6c3726aa6f2620c8c547c95bb0a5f3faef8e3eb2",
        url="https://pypi.org/packages/c1/e0/98abd4c2db9f684554306b45ef0855913e4e51f36fac74c63f393cc82080/pyem-2.1.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:")

    # pip silently replaces distutils with setuptools
