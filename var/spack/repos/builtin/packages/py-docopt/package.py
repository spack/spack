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


class PyDocopt(PythonPackage):
    """docopt creates beautiful command-line interfaces."""

    homepage = "https://github.com/docopt/docopt"
    url      = "https://github.com/docopt/docopt/archive/0.6.2.tar.gz"

    version('0.6.2', 'a6c44155426fd0f7def8b2551d02fef6')
    version('0.6.1', '98b9b74ef7f34382ce84baa7d03b3881')
    version('0.6.0', 'd2ff4f8c52e7f0d91ad2258137b625dc')
    version('0.5.0', '1c6f821ea81a8e3b37751009c3bb8269')

    depends_on('py-setuptools', type='build')
