# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAnsi2html(PythonPackage):
    """Convert text with ansi color codes to HTML"""

    homepage = "https://github.com/pycontribs/ansi2html"
    pypi = "ansi2html/ansi2html-1.6.0.tar.gz"

    maintainers("dorton21")

    license("LGPL-3.0-or-later")

    version(
        "1.6.0",
        sha256="9fa44ca8fb8c417a05a9af1c62e192694b0fcec269ab55f130b5b26e260d0b7c",
        url="https://pypi.org/packages/c6/85/3a46be84afbb16b392a138cd396117f438c7b2e91d8dc327621d1ae1b5dc/ansi2html-1.6.0-py3-none-any.whl",
    )
