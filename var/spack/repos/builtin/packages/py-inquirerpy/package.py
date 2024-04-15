# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyInquirerpy(PythonPackage):
    """Python port of Inquirer.js
    (A collection of common interactive command-line user interfaces).
    """

    homepage = "https://github.com/kazhala/InquirerPy"
    pypi = "inquirerpy/InquirerPy-0.3.4.tar.gz"

    license("MIT")

    version(
        "0.3.4",
        sha256="c65fdfbac1fa00e3ee4fb10679f4d3ed7a012abf4833910e63c295827fe2a7d4",
        url="https://pypi.org/packages/ce/ff/3b59672c47c6284e8005b42e84ceba13864aa0f39f067c973d1af02f5d91/InquirerPy-0.3.4-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:3", when="@0.2.2:")
        depends_on("py-pfzy@0.3.1:", when="@0.3:")
        depends_on("py-prompt-toolkit@3.0.1:", when="@0.2.2:")
