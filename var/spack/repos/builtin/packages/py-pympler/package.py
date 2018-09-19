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


class PyPympler(PythonPackage):
    """Development tool to measure, monitor and analyze the memory behavior
        of Python objects in a running Python application.
    """

    homepage = "https://github.com/pympler/pympler"
    url      = "https://pypi.io/packages/source/P/Pympler/Pympler-0.4.3.tar.gz"

    version('0.4.3', 'bbb4239126e9c99e2effc83b02bf8755')
    version('0.4.2', '6bdfd913ad4c94036e8a2b358e49abd7')
    version('0.4.1', '2d54032a6da91ff438f48d5f36b719a6')
    version('0.4',   '68e4a8aa4a268996fa6a321b664918af')
    version('0.3.1', '906ce437f46fb30991007671a59d4319')

    depends_on('python@2.5:')
