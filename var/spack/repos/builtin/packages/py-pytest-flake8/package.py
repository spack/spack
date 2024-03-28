# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytestFlake8(PythonPackage):
    """pytest plugin to check FLAKE8 requirements."""

    homepage = "https://github.com/tholo/pytest-flake8"
    pypi = "pytest-flake8/pytest-flake8-0.8.1.tar.gz"

    license("BSD-2-Clause")

    version(
        "0.8.1",
        sha256="8efaf4595a13079197ac740a12e6a87e3403f08133a42d3ac5984474f6f91681",
        url="https://pypi.org/packages/fb/a8/a0e52a3172f2c0dd710ab9f48929d50b95a0dcac94c562b0358153267950/pytest_flake8-0.8.1-py2.py3-none-any.whl",
    )

    # Install requires:
