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


class Geos(AutotoolsPackage):
    """GEOS (Geometry Engine - Open Source) is a C++ port of the Java
       Topology Suite (JTS). As such, it aims to contain the complete
       functionality of JTS in C++. This includes all the OpenGIS
       Simple Features for SQL spatial predicate functions and spatial
       operators, as well as specific JTS enhanced topology functions."""

    homepage = "http://trac.osgeo.org/geos/"
    url      = "http://download.osgeo.org/geos/geos-3.6.2.tar.bz2"

    version('3.6.2', 'a32142343c93d3bf151f73db3baa651f')
    version('3.6.1', 'c97e338b3bc81f9848656e9d693ca6cc')
    version('3.6.0', '55de5fdf075c608d2d7b9348179ee649')
    version('3.5.1', '2e3e1ccbd42fee9ec427106b65e43dc0')
    version('3.5.0', '136842690be7f504fba46b3c539438dd')
    version('3.4.3', '77f2c2cca1e9f49bc1bece9037ac7a7a')
    version('3.4.2', 'fc5df2d926eb7e67f988a43a92683bae')
    version('3.4.1', '4c930dec44c45c49cd71f3e0931ded7e')
    version('3.4.0', 'e41318fc76b5dc764a69d43ac6b18488')
    version('3.3.9', '4794c20f07721d5011c93efc6ccb8e4e')
    version('3.3.8', '75be476d0831a2d14958fed76ca266de')
    version('3.3.7', '95ab996d22672b067d92c7dee2170460')
    version('3.3.6', '6fadfb941541875f4976f75fb0bbc800')
    version('3.3.5', '2ba61afb7fe2c5ddf642d82d7b16e75b')
    version('3.3.4', '1bb9f14d57ef06ffa41cb1d67acb55a1')
    version('3.3.3', '8454e653d7ecca475153cc88fd1daa26')

    # Ruby bindings are fully supported
    variant('ruby',   default=False, description='Enable Ruby support')

    # Since version 3.0, the Python bindings are unsupported
    variant('python', default=False, description='Enable Python support')

    extends('ruby', when='+ruby')

    # Python 3 is supposedly supported, but I couldn't get it to work
    # https://trac.osgeo.org/geos/ticket/774
    extends('python@:2', when='+python')

    depends_on('swig', type='build', when='+ruby')
    depends_on('swig', type='build', when='+python')

    # `make check` fails with:
    # FAIL: geos_unit

    # I wasn't able to get the ruby bindings working.
    # It resulted in "Undefined symbols for architecture x86_64".

    def configure_args(self):
        spec = self.spec
        args = []

        if '+ruby' in spec:
            args.append('--enable-ruby')
        else:
            args.append('--disable-ruby')

        if '+python' in spec:
            args.append('--enable-python')
        else:
            args.append('--disable-python')

        return args
