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


class Iozone(MakefilePackage):
    """IOzone is a filesystem benchmark tool. The benchmark generates and
    measures a variety of file operations. Iozone has been ported to many
    machines and runs under many operating systems."""

    homepage = "http://www.iozone.org/"
    url      = "http://www.iozone.org/src/current/iozone3_465.tar"

    version('3_465', 'c924e5e46fb1cf8145f420e8e57eb954')

    # TODO: Add support for other architectures as necessary
    build_targets = ['linux-AMD64']

    build_directory = 'src/current'

    def edit(self, spec, prefix):
        with working_dir(self.build_directory):
            filter_file(r'^CC\t= cc',
                        r'CC\t= {0}'.format(spack_cc),
                        'makefile')

    def install(self, spec, prefix):
        install_tree('docs', join_path(prefix, 'docs'))

        with working_dir(self.build_directory):
            install_tree('.', prefix.bin)
