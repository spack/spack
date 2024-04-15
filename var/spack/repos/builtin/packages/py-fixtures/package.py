# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFixtures(PythonPackage):
    """Fixtures, reusable state for writing clean tests and more."""

    homepage = "https://launchpad.net/python-fixtures"
    pypi = "fixtures/fixtures-3.0.0.tar.gz"

    license("Apache-2.0")

    version(
        "3.0.0",
        sha256="2a551b0421101de112d9497fb5f6fd25e5019391c0fbec9bad591ecae981420d",
        url="https://pypi.org/packages/a8/28/7eed6bf76792f418029a18d5b2ace87ce7562927cdd00f1cefe481cd148f/fixtures-3.0.0-py2.py3-none-any.whl",
    )
