# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyHtml2text(PythonPackage):
    """Turn HTML into equivalent Markdown-structured text."""

    homepage = "https://github.com/Alir3z4/html2text/"
    url      = "https://pypi.io/packages/source/h/html2text/html2text-2016.9.19.tar.gz"

    version('2016.9.19', 'd6b07e32ed21f186496f012691e02dd5')

    depends_on('py-setuptools', type='build')
