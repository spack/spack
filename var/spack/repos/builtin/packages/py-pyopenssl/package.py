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


class PyPyopenssl(PythonPackage):
    """High-level wrapper around a subset of the OpenSSL library."""

    homepage = "https://pyopenssl.org/"
    url      = "https://pypi.io/packages/source/p/pyOpenSSL/pyOpenSSL-18.0.0.tar.gz"

    version('18.0.0', 'c92e9c85b520b7e153fef0f7f3c5dda7')

    depends_on('py-asn1crypto')
    depends_on('py-cffi')
    depends_on('py-cryptography@2.2.1:', when='@18.0.0:')
    depends_on('py-enum34')
    depends_on('py-idna')
    depends_on('py-ipaddress')
    depends_on('py-pycparser')
    depends_on('py-six@1.5.2:')
    depends_on('python@2.7:', when='@18.0.0:')
