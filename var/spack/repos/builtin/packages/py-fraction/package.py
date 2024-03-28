# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFraction(PythonPackage):
    """
    Fraction carries out all the fraction operations including addition, subtraction, multiplicati
    on, division, reciprocation.
    """

    homepage = "https://github.com/bradley101/fraction"
    pypi = "Fraction/Fraction-2.2.0.tar.gz"

    maintainers("LydDeb")

    license("MIT")

    version(
        "2.2.0",
        sha256="f1b7f02a03cdbf3552172174191352dbe6c9cabe0c0841a4956a49db0ce1554a",
        url="https://pypi.org/packages/58/e8/6a04edfad07782e51a7ce28b4e3240978c18b337f6d07d178e43398b8a4b/Fraction-2.2.0-py3-none-any.whl",
    )
