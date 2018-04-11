##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
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


class PyPsycopg(PythonPackage):
    """Psycopg is the most popular PostgreSQL adapter for the Python
    programming language. At its core it fully implements the Python DB API
    2.0 specifications. Several extensions allow access to many of the
    features offered by PostgreSQL."""

    homepage = "http://initd.org/psycopg/"
    url      = "http://initd.org/psycopg/tarballs/PSYCOPG-2-7/psycopg2-2.7.4.tar.gz"

    version('2.7.4',   '70fc57072e084565a42689d416cf2c5c')
    version('2.7.3.2', '8114e672d5f23fa5329874a4314fbd6f')
    version('2.7.3.1', '903e6324bd456c0e3a95aa89b8a78d72')
    version('2.7.3',   'f9823ffedcec57a8c036e67c6fb3fa36')
    version('2.7.2',   'e077aa1a79bdf1074db330968178e719')
    version('2.7.1',   '67848ac33af88336046802f6ef7081f3')
    version('2.7',     '3059253574ce96ce7f310f7b6ff98f2c')

    depends_on('py-setuptools', type='build')
    depends_on('postgresql-python')
