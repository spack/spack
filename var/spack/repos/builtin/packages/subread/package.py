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
import sys


class Subread(MakefilePackage):
    """The Subread software package is a tool kit for processing next-gen
       sequencing data."""

    homepage = "http://subread.sourceforge.net/"
    url      = "https://downloads.sourceforge.net/project/subread/subread-1.5.2/subread-1.5.2-source.tar.gz"

    version('1.6.2', '70125531737fe9ba2be83622ca236e5e')
    version('1.6.0', 'ed7e32c56bda1e769703e0a4db5a89a7')
    version('1.5.2', '817d2a46d87fcef885c8832475b8b247')

    depends_on('zlib')

    def build(self, spec, prefix):
        plat = sys.platform
        with working_dir('src'):
            if plat.startswith('linux'):
                filter_file(
                    'CC_EXEC = gcc',
                    'CC_EXEC = {0}'.format(spack_cc),
                    'Makefile.Linux'
                )
                make('-f', 'Makefile.Linux')
            elif plat.startswith('darwin'):
                make('-f', 'Makefile.MacOS')
            else:
                raise InstallError("The communication mechanism %s is not"
                                   "supported" % plat)

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
