# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWerkzeug(PythonPackage):
    """The Swiss Army knife of Python web development"""

    homepage = "http://werkzeug.pocoo.org"
    url      = "https://pypi.io/packages/source/W/Werkzeug/Werkzeug-0.11.11.tar.gz"

    version('0.11.15', sha256='455d7798ac263266dbd38d4841f7534dd35ca9c3da4a8df303f8488f38f3bcc0')
    version('0.11.11', sha256='e72c46bc14405cba7a26bd2ce28df734471bc9016bc8b4cb69466c2c14c2f7e5')

    depends_on('py-setuptools', type='build')
