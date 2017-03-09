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


class PyDill(PythonPackage):
    """Serialize all of python """

    homepage = "https://github.com/uqfoundation/dill"
    url      = "https://pypi.io/packages/source/d/dill/dill-0.2.6.zip"

    version('0.2.6', 'f8b98b15223d23431024349f2102b4f9')
    version('0.2.5', 'c9eecc32351f4934e2e67740a40397f6')
    version('0.2.4', '5d10cd1cafea38a45bcd4542f2ca3adc')
    version('0.2.3', '0b6c4f55da320893991cc32628a6e9be')
    version('0.2.2', 'a282b81a6d289f91218bba8d07f49bd8')
    version('0.2.1', 'b2354a5717da6228acae33cb13bc407b')
    version('0.2', '759002d9b71605cde2a7a052dad96b5d')

    depends_on('python@2.5:2.999,3.1:')

    depends_on('py-setuptools@0.6:', type='build')
