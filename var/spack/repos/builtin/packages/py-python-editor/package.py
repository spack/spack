# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonEditor(PythonPackage):
    """python-editor is a library that provides the editor module for
    programmatically interfacing with your system's EDITOR variable."""

    pypi = "python-editor/python-editor-1.0.4.tar.gz"

    license("Apache-2.0")

    version(
        "1.0.4",
        sha256="1bf6e860a8ad52a14c3ee1252d5dc25b2030618ed80c022598f00176adc8367d",
        url="https://pypi.org/packages/c6/d3/201fc3abe391bbae6606e6f1d598c15d367033332bd54352b12f35513717/python_editor-1.0.4-py3-none-any.whl",
    )
