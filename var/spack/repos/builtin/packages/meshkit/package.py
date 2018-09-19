##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
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
#
from spack import *


class Meshkit(AutotoolsPackage):
    """MeshKit is an open-source library of mesh generation functionality.
       Its design philosophy is two-fold: it provides a collection of
       meshing algorithms for use in real meshing problems, along with
       other tools commonly needed to support mesh generation"""

    homepage = "http://sigma.mcs.anl.gov/meshkit-library"
    url = "http://ftp.mcs.anl.gov/pub/fathom/meshkit-1.5.0.tar.gz"

    version('1.5.0',       '90b52416598ef65525ce4457a50ffe68')

    variant("mpi", default=True, description='enable mpi support')
    variant("netgen", default=False, description='enable netgen support')
    variant("debug", default=False, description='enable debug symbols')
    variant("shared", default=False, description='enable shared builds')

    depends_on('mpi', when='+mpi')
    depends_on('netgen', when='+netgen')
    depends_on('cgm')
    depends_on('moab+cgm+irel+fbigeom')

    def configure_args(self):
        spec = self.spec
        args = [
            "--with-igeom={0}".format(spec['cgm'].prefix),
            "--with-imesh={0}".format(spec['moab'].prefix)
        ]
        if '+mpi' in spec:
            args.extend([
                "--with-mpi",
                "CC={0}".format(spec['mpi'].mpicc),
                "CXX={0}".format(spec['mpi'].mpicxx),
                "FC={0}".format(spec['mpi'].mpifc)
            ])
#       FIXME without-mpi is not working
#       else:
#           args.append("--without-mpi")
        if '+netgen' in spec:
            args.append("--with-netgen={0}".format(spec['netgen'].prefix))
        else:
            args.append("--without-netgen")

        if '+debug' in spec:
            args.append("--enable-debug")
        else:
            args.append("--disable-debug")

        if '+shared' in spec:
            args.append("--enable-shared")
        else:
            args.append("--disable-shared")

        return args
