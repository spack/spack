# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFlaskCompress(PythonPackage):
    """Flask-Compress allows you to easily compress your Flask application's
    responses with gzip."""

    homepage = "https://github.com/libwilliam/flask-compress"
    url      = "https://pypi.io/packages/source/F/Flask-Compress/Flask-Compress-1.4.0.tar.gz"

    version('1.4.0', 'd997f73e4ed5793ec526c135aa765e15')

    depends_on('py-setuptools', type='build')
    depends_on('py-flask@0.9:', type=('build', 'run'))
