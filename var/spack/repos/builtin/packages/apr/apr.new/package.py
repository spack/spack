##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *

class Apr(Package):
    """Apache portable runtime."""
    homepage  = 'https://apr.apache.org/'
    url       = 'http://archive.apache.org/dist/apr/apr-1.5.2.tar.gz'

    version('1.5.2',    '98492e965963f852ab29f9e61b2ad700')

    #variant('ncurses', default=True, description='Enables the build of the ncurses gui')
    #variant('qt', default=False, description='Enables the build of cmake-gui')
    #variant('doc', default=False, description='Enables the generation of html and man page documentation')

    #depends_on('ncurses', when='+ncurses')
    #depends_on('qt', when='+qt')
    #depends_on('python@2.7.11:', when='+doc')
    #depends_on('py-sphinx', when='+doc')

    #def url_for_version(self, version):
    #    """Handle CMake's version-based custom URLs."""
    #    return 'https://cmake.org/files/v%s/cmake-%s.tar.gz' % (version.up_to(2), version)

    def install(self, spec, prefix):
        options = ['--prefix=%s' % prefix]
        configure(*options)
        make()
        make('install')
