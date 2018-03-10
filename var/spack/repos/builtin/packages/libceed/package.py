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

import os
import re


class Libceed(Package):
    """The CEED API Library: Code for Efficient Extensible Discretizations
    """

    homepage = "https://github.com/CEED/libCEED"

    version('develop', git='https://github.com/CEED/libCEED.git',
            branch='master')
    version('0.1', git='https://github.com/CEED/libCEED.git', tag='v0.1')

    variant('occa', default=True, description='Enable OCCA backends.')

    depends_on('occa@develop', when='+occa')

    phases = ['build', 'install']

    def build(self, spec, prefix):
        make('all')

    def install(self, spec, prefix):
        make('install', 'DESTDIR=%s' % prefix, parallel=False)

    @when('@0.1')
    def install(self, spec, prefix):
        mkdirp(prefix.include)
        install('ceed.h', prefix.include)
        mkdirp(prefix.lib)
        for f in os.listdir('.'):
            if re.match(r'.*\.(a|so|dylib)$', f):
                install(f, prefix.lib)
        mkdirp(prefix.lib.pkgconfig)
        install('ceed.pc', prefix.lib.pkgconfig)
