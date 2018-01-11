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


class Libfabric(AutotoolsPackage):
    """The Open Fabrics Interfaces (OFI) is a framework focused on exporting
       fabric communication services to applications."""

    homepage = "https://libfabric.org/"
    url      = "https://github.com/ofiwg/libfabric/releases/download/v1.5.0/libfabric-1.5.0.tar.gz"

    version('1.5.0', 'fda3e9b31ebe184f5157288d059672d6')
    version('1.4.2', '2009c8e0817060fb99606ddbf6c5ccf8')

    fabrics = ('psm',
               'psm2',
               'sockets',
               'verbs',
               'usnic',
               'mlx',
               'gni',
               'xpmem',
               'udp',
               'rxm',
               'rxd')

    variant(
       'fabrics',
       default='sockets',
       description='A list of enabled fabrics',
       values=fabrics,
       multi=True
    )


    variant('spackfabrics', default=False, description="""for any fabric in list of 
                         enabled fabrics, use spack dependencies instead of system
                         libraries"""
    )

    depends_on('rdma-core', when='+spackfabrics fabrics=verbs')
    depends_on('opa-psm2', when='+spackfabrics fabrics=psm2')

    def setup_environment(self, spack_env, run_env):
        spack_env.prepend_path('LIBRARY_PATH',
                             join_path(self.spec['opa-psm2'].prefix, 'usr', 'lib64'), when='+spackfabrics fabrics=psm2')
        spack_env.prepend_path('LD_LIBRARY_PATH',
                             join_path(self.spec['opa-psm2'].prefix, 'usr', 'lib64'), when='+spackfabrics fabrics=psm2')


    def configure_args(self):
        args = []

        args.extend(['--enable-%s=%s' %
                     (f, 'yes' if 'fabrics=%s' % f in self.spec else 'no')
                     for f in self.fabrics])

        args.append('--enable-psm2={0}'.format(join_path(self.spec['opa-psm2'].prefix,'usr')))

        return args
