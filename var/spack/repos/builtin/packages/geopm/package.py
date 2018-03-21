##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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
#     spack install geopm
#
# You can edit this file again by typing:
#
#     spack edit geopm
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Geopm(Package):

    """Global Extensible Open Power Manager (GEOPM) is an extensible power man-
    agement framework targeting high performance computing. The library can be
    extended to support new control algorithms and new hardware power manage-
    ment features. The GEOPM package provides built in features ranging from
    static management of power policy for each individual compute node, to dy-
    namic coordination of power policy and performance across all of the com-
    pute nodes hosting one MPI job on a portion of a distributed computing sys-
    tem. The dynamic coordination is implemented as a hierarchical control sys-
    tem for scalable communication and decentralized control. The hierarchical
    control system can optimize for various objective functions including maxi-
    mizing global application performance within a power bound. The root of the
    control hierarchy tree can communicate through shared memory with the sys-
    tem resource manage ment daemon to extend the hierarchy above the individu-
    al MPI job level and enable management of system power resources for multi-
    ple MPI jobs and multiple users by the system resource manager. The geopm
    package provides the libgeopm library, the libgeopmpolicy library, the
    geopmctl application and the geopmpolicy application. The libgeopm library
    can be called within MPI applications to enable application feedback for
    informing the control  decisions. If modification of the target application
    is not desired then the geopmctl application can be run concurrently with
    the target application. In this case, target application feedback is in-
    ferred by querying the hardware through Model Specific Registers (MSRs).
    With either method (libgeopm or geopmctl), the control hierarchy tree
    writes processor power policy through MSRs to enact policy decisions. The
    libgeopmpolicy library is used by a resource manager to set energy policy
    control parameters for MPI jobs. Some features of libgeopmpolicy are avail-
    able through the geopmpolicy application including support for static
    control."""

    homepage = "https://geopm.github.io"
    url      = "https://github.com/geopm/geopm/releases/download/v0.4.0/geopm-0.4.0.tar.gz"

    # Add additional proper versions and checksums here. "spack checksum geopm"
    version('0.4.0', 'd4cc8fffe521296dab379857d7e2064d')
    version('0.3.0', '568fd37234396fff134f8d57b60f2b83')
    version('master', git='https://github.com/geopm/geopm.git', branch='master')
    version('dev', git='https://github.com/geopm/geopm.git', branch='dev')

    # FIXME: Add dependencies if required.
    depends_on('m4', type='build')
    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool', type='build')
    depends_on('numactl', type='build')
    depends_on('mpi', type='build')

    # python dependcies for running:
    depends_on('py-pandas', type='run', when='+python')
    depends_on('py-numpy', type='run', when='+python')
    depends_on('py-natsort', type='run', when='+python')
    depends_on('py-matplotlib', type='run', when='+python')

    variant('debug', default=False, description='Enable debug.')
    variant('python', default=False, description='Using this option python dependecies are build using spack. These are required for running. It is assumed they are installed on the system. Use this only if this is not the case. (Long build time).')

    parallel = False

    def install(self, spec, prefix):
        spec = self.spec
        args = []

        args.append('--prefix=%s' % prefix)

        if '+debug' in spec:
            args.append('--enable-debug')

        if '+coverage' in spec:
            args.append('--enable-coverage')

        if '+overhead' in spec:
            args.append('--enable-overhead')

        if '+disable-procfs' in spec:
            args.append('--disable-procfs')

        if '+disable-mpi' in spec:
            args.append('--disable-mpi')

        if '+disable-fortran' in spec:
            args.append('--disable-fortran')

        if '+disable-doc' in spec:
            args.append('--disable-doc')

        if '+dependency-tracking' in spec:
            args.append('--enable-dependency-tracking')
        # else:
        #    args.append('--disable-dependency-tracking')

        if '+disable-openmp' in spec:
            args.append('--disable-openmp')

        if '+ompt' in spec:
            args.append('--enable-ompt')

        if '+gnu-ld' in spec:
            args.append('--with-gnu-ld')

        bash = which('bash')
        bash('./autogen.sh')
        configure(*args)
        make()
        make('install')
