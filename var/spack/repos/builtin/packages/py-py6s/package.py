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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-py6s
#
# You can edit this file again by typing:
#
#     spack edit py-py6s
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class PyPy6s(PythonPackage):
    """Py6S is a Python interface to the 6S Radiative Transfer Model. It allows 
       you to run many 6S simulations using a simple Python syntax, rather than 
       dealing with the rather cryptic 6S input and output files."""

    homepage = "http://py6s.rtwilson.com"
    url      = "https://files.pythonhosted.org/packages/1c/ea/fdb4fe3e289e3c14e3bdc473f6b6f595ceb476399600fab21c92db97c82a/Py6S-1.7.0.tar.gz"

    version('1.7.0', 'db0180a920ef328d3a4d7217374cccf7')

    # Add dependencies if required.
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('python', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-dateutil', type=('build', 'run'))
    depends_on('py-pysolar', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('sixs', type=('build', 'run'))


