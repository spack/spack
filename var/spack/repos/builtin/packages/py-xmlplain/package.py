# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXmlplain(PythonPackage):
    """XML as plain object module."""

    homepage = "https://github.com/guillon/xmlplain"
    pypi = "xmlplain/xmlplain-1.6.0.tar.gz"

    maintainers("LydDeb")

    license("Unlicense")

    version(
        "1.6.0",
        sha256="243c2b64febf7a13716987a4476e34833faf3f037e2533a5b94a2c19ff555c65",
        url="https://pypi.org/packages/9b/4f/0c7ef1c5cb5358577c81599a1779590741ad0e828a52087ca1dd40792b9f/xmlplain-1.6.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-ordereddict")
        depends_on("py-pyyaml")
