# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVcversioner(PythonPackage):
    """Vcversioner: Take version numbers from version control."""

    homepage = "https://github.com/habnabit/vcversioner"
    pypi = "vcversioner/vcversioner-2.16.0.0.tar.gz"

    license("ISC")

    version(
        "2.16.0.0",
        sha256="1b81bd26218944e6c86b03c7a840e058c697f014a03374296dc2f8969d1adf36",
        url="https://pypi.org/packages/5a/6b/6f5da157648cadbaf83f625c395cd23ff6be3421268b7bf54523b8d9aaab/vcversioner-2.16.0.0-py2-none-any.whl",
    )
