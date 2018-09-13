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
from spack import *


class Netgen(AutotoolsPackage):
    """NETGEN is an automatic 3d tetrahedral mesh generator. It accepts
       input from constructive solid geometry (CSG) or boundary
       representation (BRep) from STL file format. The connection to
       a geometry kernel allows the handling of IGES and STEP files.
       NETGEN contains modules for mesh optimization and hierarchical
       mesh refinement. """

    homepage = "https://ngsolve.org/"
    url = "https://gigenet.dl.sourceforge.net/project/netgen-mesher/netgen-mesher/5.3/netgen-5.3.1.tar.gz"

    version('5.3.1', 'afd5a9b0b1296c242a9c554f06af6510')

    variant("mpi", default=True, description='enable mpi support')
    variant("oce", default=False, description='enable oce geometry kernel')
    variant("gui", default=False, description='enable gui')
    variant("metis", default=False, description='use metis for partitioning')

    depends_on('zlib')
    depends_on('mpi', when='+mpi')
    depends_on('oce+X11', when='+oce')
    depends_on('metis', when='+metis')

    def url_for_version(self, version):
        url = "http://gigenet.dl.sourceforge.net/project/netgen-mesher/netgen-mesher/{0}/netgen-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    def configure_args(self):
        spec = self.spec
        args = []
        if '+mpi' in spec:
            args.extend([
                "CC={0}".format(spec['mpi'].mpicc),
                "CXX={0}".format(spec['mpi'].mpicxx)
            ])
        else:
            args.append("--without-mpi")

        if '+oce' in spec:
            args.append("--with-occ={0}".format(spec['oce'].prefix))
        #  FIXME
        # due to a bug in netgen config, when --without-occ is specified
        #   or --with-occ=no, OCC flags is turned true, and build fails
        #   later; so do not specify anything like that
        # else:
        #    args.append("--without-occ")

        if '~gui' in spec:
            args.append("--disable-gui")
        else:
            args.append("--enable-gui")
        if '+metis' in spec:
            args.append('--with-metis=%s' % spec['metis'].prefix)
        else:
            args.append("--without-metis")

        return args
