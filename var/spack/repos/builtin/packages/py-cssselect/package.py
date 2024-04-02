# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCssselect(PythonPackage):
    """Python-cssselect parses CSS3 Selectors and translate them to XPath 1.0
    expressions. Such expressions can be used in lxml or another XPath engine
    to find the matching elements in an XML or HTML document."""

    homepage = "https://github.com/scrapy/cssselect"
    url = "https://github.com/scrapy/cssselect/archive/v1.1.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "1.1.0",
        sha256="f612ee47b749c877ebae5bb77035d8f4202c6ad0f0fc1271b3c18ad6c4468ecf",
        url="https://pypi.org/packages/3b/d4/3b5c17f00cce85b9a1e6f91096e1cc8e8ede2e1be8e96b87ce1ed09e92c5/cssselect-1.1.0-py2.py3-none-any.whl",
    )
    version(
        "1.0.3",
        sha256="3b5103e8789da9e936a68d993b70df732d06b8bb9a337a05ed4eb52c17ef7206",
        url="https://pypi.org/packages/7b/44/25b7283e50585f0b4156960691d951b05d061abf4a714078393e51929b30/cssselect-1.0.3-py2.py3-none-any.whl",
    )
    version(
        "1.0.1",
        sha256="4f5f799a1d3182b04814007e9e7fc6c362f4489c7420d6b348cc901ece07ced9",
        url="https://pypi.org/packages/1d/e5/f1d410192e34b1034dba7804de5dbcdece20a883c445ad661e5ea8226b42/cssselect-1.0.1-py2.py3-none-any.whl",
    )
    version(
        "1.0.0",
        sha256="0bda987bf8d0cbd9e3a6c1468bdcc7c61e99b508894d65d30734415313d8d59f",
        url="https://pypi.org/packages/6e/51/7ef09046b16d4faea6a683946993acda4398e60c699ff8336244859e45bd/cssselect-1.0.0-py2.py3-none-any.whl",
    )
