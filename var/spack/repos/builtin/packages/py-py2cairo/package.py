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


class PyPy2cairo(PythonPackage):
    """bindings for the Cairo for Python 2,
       to be used in Python."""

    homepage = "https://pypi.python.org/pypi/pycairo"
    url      = "https://cairographics.org/releases/py2cairo-1.10.0.tar.bz2"

    version('1.10.0', '20337132c4ab06c1146ad384d55372c5')

    depends_on('cairo+X')
    depends_on('pixman')

    phases = ['configure', 'build', 'install']

    # The setup file does not accept a '--no-user-cfg' option
    no_user_cfg = False

    def setup_file(self, spec, prefix):
        return 'waf'

    def configure(self, spec, prefix):
        self.setup_py('configure', '--prefix={0}'.format(prefix))

    def install_args(self, spec, prefix):
        return []
