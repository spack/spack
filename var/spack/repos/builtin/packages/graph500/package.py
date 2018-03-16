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
#     spack install graph500
#
# You can edit this file again by typing:
#
#     spack edit graph500
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Graph500(Package):
    """Graph500 reference implementations."""

    homepage = "https://graph500.org"
    url      = "https://github.com/graph500/graph500/archive/graph500-3.0.0.tar.gz"

    version('3.0.0', 'a2ebb4783b21e2d86387a217776395e3')

    depends_on('mpi@2.0:')

    def install(self, spec, prefix):
        with working_dir('src'):
            # Patch
            edit = FileFilter('Makefile')
            edit.filter(r'^MPICC\s*=.*', 'MPICC={0}'.format(spec['mpi'].mpicc))
            # BUild
            make()
            # Install
            mkdir(prefix.bin)
            install('graph500_reference_bfs', prefix.bin)
            install('graph500_reference_bfs_sssp', prefix.bin)
            install('graph500_custom_bfs', prefix.bin)
            install('graph500_custom_bfs_sssp', prefix.bin)
