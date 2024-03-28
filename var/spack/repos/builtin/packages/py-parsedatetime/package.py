# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyParsedatetime(PythonPackage):
    """Parse human-readable date/time strings."""

    homepage = "https://github.com/bear/parsedatetime"
    pypi = "parsedatetime/parsedatetime-2.5.tar.gz"

    version(
        "2.5",
        sha256="3b835fc54e472c17ef447be37458b400e3fefdf14bb1ffdedb5d2c853acf4ba1",
        url="https://pypi.org/packages/4e/26/7612745a21452f6d822c0868ff7168dd8cf592645b2a553a177e1de43901/parsedatetime-2.5-py2-none-any.whl",
    )
