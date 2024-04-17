# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyBagit(PythonPackage):
    """bagit is a Python library and command line utility
    for working with BagIt style packages.
    """

    homepage = "https://libraryofcongress.github.io/bagit-python"
    pypi = "bagit/bagit-1.8.1.tar.gz"

    license("CC0-1.0")

    version(
        "1.8.1",
        sha256="d14dd7e373dd24d41f6748c42f123f7db77098dfa4a0125dbacb4c8bdf767c09",
        url="https://pypi.org/packages/1b/fc/58b3c209fdd383744b27914d0b88d0f9db72aa043e1475618d981d7089d9/bagit-1.8.1-py2.py3-none-any.whl",
    )
