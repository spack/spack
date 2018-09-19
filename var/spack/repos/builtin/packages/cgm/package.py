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


class Cgm(AutotoolsPackage):
    """The Common Geometry Module, Argonne (CGMA) is a code library
       which provides geometry functionality used for mesh generation and
       other applications."""
    homepage = "http://sigma.mcs.anl.gov/cgm-library"         
    url = "http://ftp.mcs.anl.gov/pub/fathom/cgm-16.0.tar.gz"

    version('16.0', 'a68aa5954d82502ff75d5eb91a29a01c')
    version('13.1.1', '4e8dbc4ba8f65767b29f985f7a23b01f')
    version('13.1.0', 'a6c7b22660f164ce893fb974f9cb2028')
    version('13.1', '95f724bda04919fc76818a5b7bc0b4ed')

    variant("mpi", default=True, description='enable mpi support')
    variant("oce", default=False, description='enable oce geometry kernel')
    variant("debug", default=False, description='enable debug symbols')
    variant("shared", default=False, description='enable shared builds')

    depends_on('mpi', when='+mpi')
    depends_on('oce+X11', when='+oce')

    def configure_args(self):
        spec = self.spec
        args = []

        if '+mpi' in spec:
            args.extend([
                "--with-mpi",
                "CC={0}".format(spec['mpi'].mpicc),
                "CXX={0}".format(spec['mpi'].mpicxx)
            ])
        else:
            args.append("--without-mpi")

        if '+oce' in spec:
            args.append("--with-occ={0}".format(spec['oce'].prefix))
        else:
            args.append("--without-occ")

        if '+debug' in spec:
            args.append("--enable-debug")

        if '+shared' in spec:
            args.append("--enable-shared")

        return args
