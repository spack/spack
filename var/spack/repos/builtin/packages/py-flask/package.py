# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFlask(PythonPackage):
    """A microframework based on Werkzeug, Jinja2 and good intentions"""

    homepage = "http://github.com/pallets/flask"
    url      = "https://pypi.io/packages/source/F/Flask/Flask-0.11.1.tar.gz"

    version('0.12.2', '97278dfdafda98ba7902e890b0289177')
    version('0.12.1', '76e9fee5c3afcf4634b9baf96c578207')
    version('0.11.1', 'd2af95d8fe79cf7da099f062dd122a08')

    depends_on('py-setuptools',         type='build')
    depends_on('py-werkzeug@0.7:',      type=('build', 'run'))
    depends_on('py-jinja2@2.4:',        type=('build', 'run'))
    depends_on('py-itsdangerous@0.21:', type=('build', 'run'))
    depends_on('py-click@2.0:',         type=('build', 'run'))
