# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPyxlsb(PythonPackage):
    """Excel 2007-2010 Binary Workbook (xlsb) parser"""

    pypi = "pyxlsb/pyxlsb-1.0.10.tar.gz"

    license("LGPL-3.0-only")

    version(
        "1.0.10",
        sha256="87c122a9a622e35ca5e741d2e541201d28af00fb46bec492cfa9586890b120b4",
        url="https://pypi.org/packages/7e/92/345823838ae367c59b63e03aef9c331f485370f9df6d049256a61a28f06d/pyxlsb-1.0.10-py2.py3-none-any.whl",
    )
    version(
        "1.0.8",
        sha256="7e27f68585110b38ced5b54bc904afbea2065671cf650f1c7be10dac7fca1a8a",
        url="https://pypi.org/packages/ee/a5/d40f4cf117ffd8ca0622a08c4dd1ad238e3d6252ad78594d76b3592944cb/pyxlsb-1.0.8-py2.py3-none-any.whl",
    )
    version(
        "1.0.6",
        sha256="28ae4cb0a37c525723093561057e81afb7b5b6c7f8e5f7cbfbab54fa0b6313d2",
        url="https://pypi.org/packages/e0/6f/e3af29713106b529641818a49af9982ca520755882acab0f112a7762f140/pyxlsb-1.0.6-py2.py3-none-any.whl",
    )
