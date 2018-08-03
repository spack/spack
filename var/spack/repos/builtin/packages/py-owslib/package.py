##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class PyOwslib(PythonPackage):
    """OWSLib is a Python package for client programming with Open Geospatial
    Consortium (OGC) web service (hence OWS) interface standards, and their
    related content models."""

    homepage = "http://http://geopython.github.io/OWSLib/#installation"
    url      = "https://pypi.io/packages/source/O/OWSLib/OWSLib-0.16.0.tar.gz"

    version('0.16.0', '7ff9c9edde95eadeb27ea8d8fbd1a2cf')

    depends_on('py-setuptools',     type='build')
    depends_on('py-dateutil@1.5:',  type=('build', 'run'))
    depends_on('py-pytz',           type=('build', 'run'))
    depends_on('py-requests@1.0:',  type=('build', 'run'))
    depends_on('py-proj',           type=('build', 'run'))
