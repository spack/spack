# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNosexcover(PythonPackage):
    """A companion to the built-in nose.plugins.cover, this plugin will write
    out an XML coverage report to a file named coverage.xml."""

    homepage = "https://github.com/cmheisel/nose-xcover"
    pypi = "nosexcover/nosexcover-1.0.11.tar.gz"

    version(
        "1.0.11",
        sha256="445de3e7f0b2d1bf0b53ac21aa924870eb2b46cc1aa4cc91629639a606b39177",
        url="https://pypi.org/packages/f5/74/0dfbedcab931df02d9437820014fd6f4b539b3aa64dbb8e7a362fe20343d/nosexcover-1.0.11-py2.py3-none-any.whl",
    )
