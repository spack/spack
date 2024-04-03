# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTextUnidecode(PythonPackage):
    """text-unidecode is the most basic port of the Text::Unidecode Perl
    library."""

    homepage = "https://github.com/kmike/text-unidecode/"
    pypi = "text-unidecode/text-unidecode-1.3.tar.gz"

    license("Artistic-1.0-Perl")

    version(
        "1.3",
        sha256="1311f10e8b895935241623731c2ba64f4c455287888b18189350b67134a822e8",
        url="https://pypi.org/packages/a6/a5/c0b6468d3824fe3fde30dbb5e1f687b291608f9473681bbf7dabbf5a87d7/text_unidecode-1.3-py2.py3-none-any.whl",
    )
