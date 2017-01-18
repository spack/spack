##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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

    homepage = "http://www.antlr.org"
    url      = "https://github.com/antlr/antlr/tarball/v2.7.7"

    # Notes from http://nco.sourceforge.net/#bld
    # The first steps to build (i.e., compile, for the most part) NCO from
    # source code are to install the pre-requisites: ANTLR version 2.7.7
    # (like this one not version 3.x or 4.x!) (required for ncap2)... ANTLR
    # binaries from major distributions are pre-built with the source patch
    # necessary to allow NCO to link to ANTLR... The ANTLR source file
    # CharScanner.hpp must include this line: #include <cstring> or else
    # ncap2 will not compile (this tarball is already patched).
    version('2.7.7', '914865e853fe8e1e61a9f23d045cb4ab',
            # Patched version as described above
            url='http://dust.ess.uci.edu/tmp/antlr-2.7.7.tar.gz')
    # Unpatched version
    # url='http://dust.ess.uci.edu/nco/antlr-2.7.7.tar.gz')

    variant('cxx',    default=True,  description='Enable ANTLR for C++')
    variant('java',   default=False, description='Enable ANTLR for Java')
    variant('python', default=False, description='Enable ANTLR for Python')

    extends('python', when='+python')
    depends_on('jdk', type=('build', 'run'), when='+java')

    def configure_args(self):
        spec = self.spec

        return [
            '--{0}-cxx'.format('enable' if '+cxx' in spec else 'disable'),
            '--{0}-java'.format('enable' if '+java' in spec else 'disable'),
            '--{0}-python'.format('enable' if '+python' in spec else 'disable')
        ]
