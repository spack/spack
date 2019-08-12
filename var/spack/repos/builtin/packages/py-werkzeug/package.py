# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWerkzeug(PythonPackage):
    """The Swiss Army knife of Python web development"""

    homepage = "http://werkzeug.pocoo.org"
    url      = "https://pypi.io/packages/source/W/Werkzeug/Werkzeug-0.11.11.tar.gz"

    version('0.11.15', 'cb4010478dd33905f95920e4880204a2')
    version('0.11.11', '1d34afa1f19abcef4c0da51ebc2c4ea7')

    depends_on('py-setuptools', type='build')
