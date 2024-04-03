# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXmltodict(PythonPackage):
    """xmltodict is a Python module that makes working with XML feel like
    you are working with JSON."""

    homepage = "https://github.com/martinblech/xmltodict"
    pypi = "xmltodict/xmltodict-0.12.0.tar.gz"

    license("MIT")

    version(
        "0.12.0",
        sha256="8bbcb45cc982f48b2ca8fe7e7827c5d792f217ecf1792626f808bf41c3b86051",
        url="https://pypi.org/packages/28/fd/30d5c1d3ac29ce229f6bdc40bbc20b28f716e8b363140c26eff19122d8a5/xmltodict-0.12.0-py2.py3-none-any.whl",
    )
