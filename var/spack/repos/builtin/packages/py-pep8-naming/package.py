# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPep8Naming(PythonPackage):
    """Check PEP-8 naming conventions, plugin for flake8."""

    homepage = "https://github.com/PyCQA/pep8-naming"
    pypi = "pep8-naming/pep8-naming-0.10.0.tar.gz"

    license("MIT")

    version(
        "0.10.0",
        sha256="5d9f1056cb9427ce344e98d1a7f5665710e2f20f748438e308995852cfa24164",
        url="https://pypi.org/packages/5b/69/6018efb8ae18bd5a05f5f447666060a44aa8fe017f439c50fe8c8bd990cf/pep8_naming-0.10.0-py2.py3-none-any.whl",
    )
    version(
        "0.7.0",
        sha256="360308d2c5d2fff8031c1b284820fbdb27a63274c0c1a8ce884d631836da4bdd",
        url="https://pypi.org/packages/39/bb/a34544c789e7e5458ed2db6cbd1c8e227bb01e4ce03a0b15ec4ec93e486d/pep8_naming-0.7.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-flake8-polyfill@1.0.2:", when="@0.5:0.12")
