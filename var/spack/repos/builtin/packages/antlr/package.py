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


class Antlr(AutotoolsPackage):
    """ANTLR (ANother Tool for Language Recognition) is a powerful parser
    generator for reading, processing, executing, or translating structured
    text or binary files. It's widely used to build languages, tools, and
    frameworks. From a grammar, ANTLR generates a parser that can build and
    walk parse trees."""

    homepage = "http://www.antlr2.org/"
    url      = "http://www.antlr2.org/download/antlr-2.7.7.tar.gz"

    version('2.7.7', '01cc9a2a454dd33dcd8c856ec89af090')

    # Fixes build with recent versions of GCC
    patch('gcc.patch')

    variant('cxx',    default=True,  description='Enable ANTLR for C++')
    variant('java',   default=False, description='Enable ANTLR for Java')
    variant('python', default=False, description='Enable ANTLR for Python')

    extends('python', when='+python')
    depends_on('java', type=('build', 'run'), when='+java')

    def configure_args(self):
        spec = self.spec

        return [
            '--disable-csharp',
            '--{0}-cxx'.format('enable' if '+cxx' in spec else 'disable'),
            '--{0}-java'.format('enable' if '+java' in spec else 'disable'),
            '--{0}-python'.format('enable' if '+python' in spec else 'disable')
        ]
