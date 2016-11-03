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

    variant('python', default=False, description='Provide python bindings')
    variant('perl', default=False, description='Provide Perl bindings')
    # variant('ruby', default=False, description='Provide ruby bindings')

    depends_on('apr')
    depends_on('apr-util')
    depends_on('zlib')
    depends_on('sqlite')
    depends_on('serf')
    depends_on('expat')
    depends_on('swig@:2.99')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool', type='build')
    depends_on('pkg-config', type='build')

    # Optional: We need swig if we want the Perl, Python or Ruby bindings.
    extends('python', when='+python')
    depends_on('perl@5.8:', when='+perl')
    # depends_on('ruby', when='+ruby')

    # Installation has race cases.
    parallel = False

    # helper function to locate python's site-packages directory.
    def python_sp_dir(self):
        python_version = 'python' + self.spec['python'].version.up_to(2)
        return join_path(spec['python'].prefix.lib, python_version,
                         'site-packages')

    def install(self, spec, prefix):

        # Pre-configure setup
        sh = which('sh')
        sh('./autogen.sh')

        # configure, build, install:
        options = ['--prefix=%s' % prefix]
        options.append('--with-apr=%s' % spec['apr'].prefix)
        options.append('--with-apr-util=%s' % spec['apr-util'].prefix)
        options.append('--with-zlib=%s' % spec['zlib'].prefix)
        options.append('--with-sqlite=%s' % spec['sqlite'].prefix)
        options.append('--with-serf=%s' % spec['serf'].prefix)
        options.append('--with-expat=%s:%s:expat' %
                       (spec['expat'].prefix.include,
                        spec['expat'].prefix.lib))
        options.append('--with-swig=%s' % spec['swig'].prefix)

        configure(*options)
        make()
        make('install')

        # python bindings
        if '+python' in spec:
            site_packages_dir = self.python_sp_dir
            make('swig-py')
            make('install-swig-py',
                 'swig-pydir=%s/libsvn' % site_packages_dir,
                 'swig_pydir_extra=%s/svn' % site_packages_dir)

        # perl bindings
        if '+perl' in spec:
            make('swig-pl')
            # make('check-swig-pl')
            make('install-swig-pl')

        # ruby bindings
        # if '+ruby' in spec:
            # make('swig-rb')
            # make('install-swig-rb')
