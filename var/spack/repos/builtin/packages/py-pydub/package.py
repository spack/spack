# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPydub(PythonPackage):
    """Manipulate audio with an simple and easy high level interface"""

    homepage = "http://pydub.com/"
    pypi = "pydub/pydub-0.25.1.tar.gz"

    license("MIT")

    version(
        "0.25.1",
        sha256="65617e33033874b59d87db603aa1ed450633288aefead953b30bded59cb599a6",
        url="https://pypi.org/packages/a6/53/d78dc063216e62fc55f6b2eebb447f6a4b0a59f55c8406376f76bf959b08/pydub-0.25.1-py2.py3-none-any.whl",
    )
