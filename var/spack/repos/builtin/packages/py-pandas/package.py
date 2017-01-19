##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class PyPandas(PythonPackage):
    """pandas is a Python package providing fast, flexible, and expressive
       data structures designed to make working with relational or
       labeled data both easy and intuitive. It aims to be the
       fundamental high-level building block for doing practical, real
       world data analysis in Python. Additionally, it has the broader
       goal of becoming the most powerful and flexible open source data
       analysis / manipulation tool available in any language.

    """
    homepage = "http://pandas.pydata.org/"
    url      = "https://pypi.python.org/packages/source/p/pandas/pandas-0.16.0.tar.gz#md5=bfe311f05dc0c351f8955fbd1e296e73"

    version('0.16.0', 'bfe311f05dc0c351f8955fbd1e296e73')
    version('0.16.1', 'fac4f25748f9610a3e00e765474bdea8')
    version('0.18.0', 'f143762cd7a59815e348adf4308d2cf6')

    depends_on('py-dateutil', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-pytz', type=('build', 'run'))
    depends_on('py-numexpr', type=('build', 'run'))
    depends_on('py-bottleneck', type=('build', 'run'))
