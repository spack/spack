# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# ----------------------------------------------------------------------------
from spack.package import *


class PyRequirementsParser(PythonPackage):
    """This is a small Python module for parsing Pip requirement files.
    The goal is to parse everything in the Pip requirement file format spec."""

    homepage = "https://github.com/madpah/requirements-parser"
    pypi = "requirements-parser/requirements-parser-0.5.0.tar.gz"

    maintainers("DaxLynch", "eugeneswalker")

    license("Apache-2.0")

    version(
        "0.5.0",
        sha256="e7fcdcd04f2049e73a9fb150d8a0f9d51ce4108f5f7cbeac74c484e17b12bcd9",
        url="https://pypi.org/packages/f8/89/612e3b326d87780dc1daf39af7696634f969838213cddae4f553f75d04ae/requirements_parser-0.5.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3", when="@0.3:")
        depends_on("py-types-setuptools", when="@0.4:")
