# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyOwslib(PythonPackage):
    """OWSLib is a Python package for client programming with Open Geospatial
    Consortium (OGC) web service (hence OWS) interface standards, and their
    related content models."""

    homepage = "http://http://geopython.github.io/OWSLib/#installation"
    url      = "https://pypi.io/packages/source/O/OWSLib/OWSLib-0.16.0.tar.gz"

    version('0.16.0', '7ff9c9edde95eadeb27ea8d8fbd1a2cf')

    depends_on('py-setuptools',     type='build')
    depends_on('py-python-dateutil@1.5:',  type=('build', 'run'))
    depends_on('py-pytz',           type=('build', 'run'))
    depends_on('py-requests@1.0:',  type=('build', 'run'))
    depends_on('py-pyproj',           type=('build', 'run'))
