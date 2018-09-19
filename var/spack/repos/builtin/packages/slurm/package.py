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


class Slurm(AutotoolsPackage):
    """Slurm is an open source, fault-tolerant, and highly scalable cluster
    management and job scheduling system for large and small Linux clusters.

    Slurm requires no kernel modifications for its operation and is relatively
    self-contained. As a cluster workload manager, Slurm has three key
    functions. First, it allocates exclusive and/or non-exclusive access to
    resources (compute nodes) to users for some duration of time so they can
    perform work. Second, it provides a framework for starting, executing,
    and monitoring work (normally a parallel job) on the set of allocated
    nodes. Finally, it arbitrates contention for resources by managing a
    queue of pending work.
    """

    homepage = 'https://slurm.schedmd.com'
    url = 'https://github.com/SchedMD/slurm/archive/slurm-17-02-6-1.tar.gz'

    version('17-02-6-1', '8edbb9ad41819464350d9de013367020')

    variant('gtk', default=False, description='Enable GTK+ support')
    variant('mariadb', default=False, description='Use MariaDB instead of MySQL')

    variant('hwloc', default=False, description='Enable hwloc support')
    variant('hdf5', default=False, description='Enable hdf5 support')
    variant('readline', default=True, description='Enable readline support')

    # TODO: add variant for BG/Q and Cray support

    # TODO: add support for checkpoint/restart (BLCR)

    # TODO: add support for lua

    depends_on('curl')
    depends_on('glib')
    depends_on('json-c')
    depends_on('lz4')
    depends_on('munge')
    depends_on('openssl')
    depends_on('pkgconfig', type='build')
    depends_on('readline', when='+readline')
    depends_on('zlib')

    depends_on('gtkplus', when='+gtk')
    depends_on('hdf5', when='+hdf5')
    depends_on('hwloc', when='+hwloc')
    depends_on('mariadb', when='+mariadb')

    def configure_args(self):

        spec = self.spec

        args = [
            '--with-libcurl={0}'.format(spec['curl'].prefix),
            '--with-json={0}'.format(spec['json-c'].prefix),
            '--with-lz4={0}'.format(spec['lz4'].prefix),
            '--with-munge={0}'.format(spec['munge'].prefix),
            '--with-ssl={0}'.format(spec['openssl'].prefix),
            '--with-zlib={0}'.format(spec['zlib'].prefix),
        ]

        if '~gtk' in spec:
            args.append('--disable-gtktest')

        if '~readline' in spec:
            args.append('--without-readline')

        if '+hdf5' in spec:
            args.append(
                '--with-hdf5={0}'.format(spec['hdf5'].prefix.bin.h5cc)
            )
        else:
            args.append('--without-hdf5')

        if '+hwloc' in spec:
            args.append('--with-hwloc={0}'.format(spec['hwloc'].prefix))
        else:
            args.append('--without-hwloc')

        return args
