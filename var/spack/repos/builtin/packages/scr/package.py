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

import os


class Scr(CMakePackage):
    """SCR caches checkpoint data in storage on the compute nodes of a
       Linux cluster to provide a fast, scalable checkpoint/restart
       capability for MPI codes"""

    homepage = "http://computation.llnl.gov/projects/scalable-checkpoint-restart-for-mpi"
    url      = "https://github.com/LLNL/scr/archive/v1.2.0.tar.gz"
    git      = "https://github.com/llnl/scr.git"

    # NOTE: scr-v1.1.8 is built with autotools and is not properly build here.
    # scr-v1.1.8 will be deprecated with the upcoming release of v1.2.0
    # url      = "https://github.com/LLNL/scr/releases/download/v1.1.8/scr-1.1.8.tar.gz"
    # version('1.1.8', '6a0f11ad18e27fcfc00a271ff587b06e')

    version('master', branch='master')
    version('1.2.0', '060e9e9c7604c1765f3991f9cd6e9d2d')

    depends_on('pdsh+static_modules', type=('build', 'run'))
    depends_on('zlib')
    depends_on('mpi')

    variant('dtcmp', default=True,
            description="Build with DTCMP. "
            "Necessary to enable user directory naming at runtime")
    depends_on('dtcmp', when="+dtcmp")

    variant('libyogrt', default=True,
            description="Build SCR with libyogrt for get_time_remaining.")
    depends_on('libyogrt', when="+libyogrt")

    # MySQL not yet in spack
    # variant('mysql', default=True, decription="MySQL database for logging")
    # depends_on('mysql', when="+mysql")

    variant('scr_config', default='scr.conf',
            description='Location for SCR to find its system config file. '
            'May be either absolute or relative to the install prefix')
    variant('copy_config', default=None,
            description='Location from which to copy SCR system config file. '
            'Must be an absolute path.')

    variant('fortran', default=True,
            description="Build SCR with fortran bindings")

    variant('resource_manager', default='SLURM',
            values=('SLURM', 'APRUN', 'PMIX', 'LSF', 'NONE'),
            multi=False,
            description="Resource manager for which to configure SCR.")

    variant('async_api', default='NONE',
            values=('NONE', 'CRAY_DW', 'IBM_BBAPI', 'INTEL_CPPR'),
            multi=False,
            description="Asynchronous data transfer API to use with SCR.")

    variant('file_lock', default='FLOCK',
            values=('FLOCK', 'FNCTL', 'NONE'),
            multi=False,
            description='File locking style for SCR.')

    variant('cache_base', default='/tmp',
            description='Compile time default location for checkpoint cache.')
    variant('cntl_base', default='/tmp',
            description='Compile time default location for control directory.')

    conflicts('platform=bgq')

    def get_abs_path_rel_prefix(self, path):
        # Return path if absolute, otherwise prepend prefix
        if os.path.isabs(path):
            return path
        else:
            return join_path(self.spec.prefix, path)

    def cmake_args(self):
        spec = self.spec
        args = []

        if 'platform=cray' in spec:
            args.append('-DSCR_LINK_STATIC=ON')

        args.append('-DENABLE_FORTRAN={0}'.format('+fortran' in spec))

        conf_path = self.get_abs_path_rel_prefix(
            self.spec.variants['scr_config'].value)
        args.append('-DCMAKE_SCR_CONFIG_FILE={0}'.format(conf_path))

        # We uppercase the values for these to avoid unnecessary user error.
        args.append('-DSCR_RESOURCE_MANAGER={0}'.format(
            spec.variants['resource_manager'].value.upper()))

        args.append('-DSCR_ASYNC_API={0}'.format(
            spec.variants['async_api'].value.upper()))

        args.append('-DSCR_FILE_LOCK={0}'.format(
            spec.variants['file_lock'].value.upper()))

        args.append('-DSCR_CACHE_BASE={0}'.format(
            spec.variants['cache_base'].value))

        args.append('-DSCR_CNTL_BASE={0}'.format(
            spec.variants['cntl_base'].value))

        args.append('-DWITH_PDSH_PREFIX={0}'.format(spec['pdsh'].prefix))

        if "+dtcmp" in spec:
            args.append('-DWITH_DTCMP_PREFIX={0}'.format(spec['dtcmp'].prefix))

        if "+libyogrt" in spec:
            args.append('-DWITH_YOGRT_PREFIX={0}'.format(
                spec['libyogrt'].prefix))

        # if "+mysql" in spec:
        # args.append('-DWITH_MYSQL_PREFIX={0}'.format(
        # spec['mysql'].prefix))

        return args

    @run_after('install')
    def copy_config(self):
        spec = self.spec
        if spec.variants['copy_config'].value:
            dest_path = self.get_abs_path_rel_prefix(
                spec.variants['scr_config'].value)
            install(spec.variants['copy_config'].value, dest_path)
