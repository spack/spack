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


class Canu(MakefilePackage):
    """A single molecule sequence assembler for genomes large and
       small."""

    homepage = "http://canu.readthedocs.io/"
    url      = "https://github.com/marbl/canu/archive/v1.5.tar.gz"

    version('1.5', '65df275baa28ecf11b15dfd7343361e3')

    depends_on('gnuplot', type='run')
    depends_on('jdk', type='run')
    depends_on('perl', type='run')

    build_directory = 'src'

    def patch(self):
        # Use our perl, not whatever is in the environment
        filter_file(r'^#!/usr/bin/env perl',
                    '#!{0}'.format(self.spec['perl'].command.path),
                    'src/pipelines/canu.pl')

    def install(self, spec, prefix):
        # replicate the Makefile logic here:
        # https://github.com/marbl/canu/blob/master/src/Makefile#L344
        uname = which('uname')
        ostype = uname(output=str).strip()
        machinetype = uname('-m', output=str).strip()
        if machinetype == 'x86_64':
            machinetype = 'amd64'
        target_dir = '{0}-{1}'.format(ostype, machinetype)
        bin = join_path(target_dir, 'bin')

        install_tree(bin, prefix.bin)
