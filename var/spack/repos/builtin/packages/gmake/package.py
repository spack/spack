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
from spack import *


class Gmake(AutotoolsPackage):
    """GNU Make is a tool which controls the generation of executables and
    other non-source files of a program from the program's source files."""

    homepage = "https://www.gnu.org/software/make/"
    url      = "https://ftp.gnu.org/gnu/make/make-4.2.1.tar.gz"

    version('4.2.1', '7d0dcb6c474b258aab4d54098f2cf5a7')
    version('4.0',   'b5e558f981326d9ca1bfdb841640721a')

    variant('guile', default=False, description='Support GNU Guile for embedded scripting')

    depends_on('guile', when='+guile')

    build_directory = 'spack-build'

    def configure_args(self):
        args = []

        if '+guile' in self.spec:
            args.append('--with-guile')
        else:
            args.append('--without-guile')

        return args

    @run_after('install')
    def symlink_gmake(self):
        with working_dir(self.prefix.bin):
            symlink('make', 'gmake')
