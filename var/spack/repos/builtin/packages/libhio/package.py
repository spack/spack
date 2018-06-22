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


class Libhio(AutotoolsPackage):
    """libHIO is a flexible, high-performance parallel IO package developed
       at LANL.  libHIO supports IO to either a conventional PFS or to Cray
       DataWarp with management of Cray DataWarp space and stage-in and
       stage-out from and to the PFS.
    """

    homepage = "https://github.com/hpc/libhio"
    url      = "https://github.com/hpc/libhio/releases/download/hio.1.4.1.0/libhio-1.4.1.0.tar.bz2"

    #
    # We don't include older versions since they are missing features
    # needed by current and future consumers of libhio
    #
    version('1.4.1.2', '38c7d33210155e5796b16d536d1b5cfe')
    version('1.4.1.0', '6ef566fd8cf31fdcd05fab01dd3fae44')

    #
    # main users of libhio thru spack will want to use HFDF5 plugin,
    # so make hdf5 variant a default
    #
    variant('hdf5', default=True, description='Enable HDF5 support')

    depends_on("json-c")
    depends_on("bzip2")
    depends_on("pkgconfig", type="build")
    depends_on('mpi')

    #
    # libhio depends on hdf5+mpi if hdf5 is being used since it
    # autodetects the presence of an MPI and/or uses mpicc by default to build
    depends_on('hdf5+mpi', when='+hdf5')

    #
    # wow, we need to patch libhio
    #
    patch('0001-configury-fix-a-problem-with-bz2-configury.patch', when="@1.4.1.0")
    patch('0001-hdf5-make-docs-optional.patch', when="@1.4.1.0")

    def autoreconf(self, spec, prefix):
        autoreconf = which('autoreconf')
        autoreconf('-ifv')

    def configure_args(self):
        spec = self.spec
        args = []

        args.append('--with-external_bz2={0}'.format(spec['bzip2'].prefix))
        if '+hdf5' in spec:
            args.append('--with-hdf5={0}'.format(spec['hdf5'].prefix))
        return args
