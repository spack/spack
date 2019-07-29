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
#     spack install py-pysolar
#
# You can edit this file again by typing:
#
#     spack edit py-pysolar
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class PyPysolar(PythonPackage):
    """Pysolar is a collection of Python libraries for simulating the 
       irradiation of any point on earth by the sun. It includes code 
       for extremely precise ephemeris calculations, and more."""

    # Add a proper url for your package's homepage here.
    homepage = "http://pysolar.readthedocs.io"
    url      = "https://github.com/pingswept/pysolar/archive/0.6.tar.gz"

    #version('0.8-RC1',   '6b873ed7126e891235ffde9403baef96')
    #version('0.7',       'ba3da20882ac3964f59a1f5a0bc2ac17')
    version('0.6',       '78005c1e498100cc30842af20ca76069')
    version('0.5',       'af0b7ae297d90a5fee51c4a7a559f902')
    version('0.4.4',     'b9686f13500e537966834c2178944bde')
    version('0.4.3',     '6cb5e04e4bb85ea2bc49927cb3a937d3')
    version('0.4.2',     '086ca926d03a7fb395b4022d5ac6c8b8')
    version('0.4.1',     '2a8dd536957da3f512d9d91e6ca2c770')
    version('0.4.0',     '4aaa184ff5505a89a5c4ea744dd64b8f')

    # Add dependencies if required.
    depends_on('py-setuptools', type='build')

