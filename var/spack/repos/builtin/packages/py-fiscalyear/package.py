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


class PyFiscalyear(PythonPackage):
    """fiscalyear is a small, lightweight Python module providing helpful
    utilities for managing the fiscal calendar. It is designed as an extension
    of the built-in datetime and calendar modules, adding the ability to query
    the fiscal year and fiscal quarter of a date or datetime object."""

    homepage = "https://github.com/adamjstewart/fiscalyear"
    url      = "https://pypi.io/packages/source/f/fiscalyear/fiscalyear-0.1.0.tar.gz"
    git      = "https://github.com/adamjstewart/fiscalyear.git"

    maintainers = ['adamjstewart']
    import_modules = ['fiscalyear']

    version('master', branch='master')
    version('0.1.0', '30e36b259f3e72e4929abbf259335742')

    depends_on('python@2.5:')
    depends_on('py-setuptools', type='build')

    depends_on('py-pytest', type='test')
    depends_on('py-pytest-runner', type='test')
