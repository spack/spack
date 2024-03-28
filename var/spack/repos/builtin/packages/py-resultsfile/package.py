# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyResultsfile(PythonPackage):
    """Python module to read output files of quantum chemistry programs"""

    homepage = "https://gitlab.com/scemama/resultsFile"
    url = "https://gitlab.com/scemama/resultsFile/-/archive/v1.0/resultsFile-v1.0.tar.gz"
    git = "https://gitlab.com/scemama/resultsFile.git"

    maintainers("scemama")

    license("GPL-2.0-only")

    version(
        "2.0",
        sha256="4a560e17e972088865e9f9717726cf4fc831135b94ad576ed2a472332e6281e4",
        url="https://pypi.org/packages/ff/66/1a98fa07dd9c3cebc94866e302bf16f7b0a316709ae36b2e809577cbc354/resultsFile-2.0-py3-none-any.whl",
    )

    # pip silently replaces distutils with setuptools
