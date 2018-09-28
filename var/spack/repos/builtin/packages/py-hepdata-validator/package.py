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


class PyHepdataValidator(PythonPackage):
    """Validation schema and code for HEPdata submissions."""

    homepage = "https://github.com/hepdata/hepdata-validator"
    url = "https://pypi.io/packages/source/h/hepdata_validator/hepdata_validator-0.1.16.tar.gz"

    version('0.1.16', '62e80db7425a4a48050af29e05295e0d')
    version('0.1.15', 'e29aa75780b9963997e79f572ca0209f')
    version('0.1.14', '386a2440f23fda7d877764d120bf61fb')
    version('0.1.8', '5bf388a507a857afbe0deba0857125c7')

    depends_on('py-setuptools', type='build')
    depends_on('py-jsonschema', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
