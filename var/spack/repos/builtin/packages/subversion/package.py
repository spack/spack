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


class Subversion(Package):
    """Apache Subversion - an open source version control system."""
    homepage  = 'https://subversion.apache.org/'
    url       = 'http://archive.apache.org/dist/subversion/subversion-1.8.13.tar.gz'

    version('1.8.13',    '8065b3698d799507fb72dd7926ed32b6')
    version('1.9.3',     'a92bcfaec4e5038f82c74a7b5bbd2f46')

    depends_on('apr')
    depends_on('apr-util')
    depends_on('zlib')
    depends_on('sqlite')
    depends_on('serf')

    # Optional: We need swig if we want the Perl, Python or Ruby
    # bindings.
    # depends_on('swig')
    # depends_on('python')
    # depends_on('perl')
    # depends_on('ruby')

    # Installation has race cases.
    parallel = False

    def install(self, spec, prefix):

        # configure, build, install:
        # Ref:
        # http://www.linuxfromscratch.org/blfs/view/svn/general/subversion.html
        options = ['--prefix=%s' % prefix]
        options.append('--with-apr=%s' % spec['apr'].prefix)
        options.append('--with-apr-util=%s' % spec['apr-util'].prefix)
        options.append('--with-zlib=%s' % spec['zlib'].prefix)
        options.append('--with-sqlite=%s' % spec['sqlite'].prefix)
        options.append('--with-serf=%s' % spec['serf'].prefix)
        # options.append('--with-swig=%s' % spec['swig'].prefix)

        configure(*options)
        make()
        make('install')

        # python bindings
        # make('swig-py',
        #     'swig-pydir=/usr/lib/python2.7/site-packages/libsvn',
        #     'swig_pydir_extra=/usr/lib/python2.7/site-packages/svn')
        # make('install-swig-py',
        #     'swig-pydir=/usr/lib/python2.7/site-packages/libsvn',
        #     'swig_pydir_extra=/usr/lib/python2.7/site-packages/svn')

        # perl bindings
        # make('swig-pl')
        # make('install-swig-pl')

        # ruby bindings
        # make('swig-rb')
        # make('isntall-swig-rb')
