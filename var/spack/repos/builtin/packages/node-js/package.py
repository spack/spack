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
import subprocess


class NodeJs(Package):
    """Node.js is a JavaScript runtime built on Chrome's V8 JavaScript
    engine."""

    homepage = "https://nodejs.org/"
    url      = "https://nodejs.org/download/release/v6.3.0/node-v6.3.0.tar.gz"

    version('8.9.1', '7482b2523f72000d1b6060c38945026b')
    version('7.1.0', '1db5df2cb025f9c70e83d9cf21c4266a')
    version('6.3.0', '8c14e5c89d66d4d060c91b3ba15dfd31')
    version('6.2.2', '1120e8bf191fdaee42206d031935210d')

    # variant('bash-completion', default=False, description='Build with bash-completion support for npm')  # NOQA: ignore=E501
    variant('debug', default=False, description='Include debugger support')
    variant('doc', default=False, description='Compile with documentation')
    variant('icu4c', default=False, description='Build with support for all locales instead of just English')
    variant('openssl', default=True,  description='Build with Spacks OpenSSL instead of the bundled version')
    variant('zlib', default=True,  description='Build with Spacks zlib instead of the bundled version')

    depends_on('libtool', type='build', when=sys.platform != 'darwin')
    depends_on('pkgconfig', type='build')
    depends_on('python@2.7:2.8', type='build')
    # depends_on('bash-completion', when="+bash-completion")
    depends_on('icu4c', when='+icu4c')
    depends_on('openssl@1.0.2d:', when='+openssl')

    def install(self, spec, prefix):
        options = []
        options.extend(['--prefix={0}'.format(prefix)])

        # Note: npm is updated more regularly than node.js, so we build the
        #       package instead of using the bundled version
        options.extend(['--without-npm'])

        # On OSX, the system libtool must be used
        # So, we ensure that this is the case by...
        if sys.platform == 'darwin':
            process_pipe = subprocess.Popen(["which", "libtool"],
                                            stdout=subprocess.PIPE)
            result_which = process_pipe.communicate()[0]
            process_pipe = subprocess.Popen(["whereis", "libtool"],
                                            stdout=subprocess.PIPE)
            result_whereis = process_pipe.communicate()[0]
            assert result_which == result_whereis, (
                'On OSX the system libtool must be used. Please'
                '(temporarily) remove \n %s or its link to libtool from'
                'path')

        # TODO: Add bash-completion

        if '+debug' in spec:
            options.extend(['--debug'])

        if '+openssl' in spec:
            options.extend([
                '--shared-openssl',
                '--shared-openssl-includes=%s' % spec['openssl'].prefix.include,  # NOQA: ignore=E501
                '--shared-openssl-libpath=%s' % spec['openssl'].prefix.lib,
            ])

        if '+zlib' in spec:
            options.extend([
                '--shared-zlib',
                '--shared-zlib-includes=%s' % spec['zlib'].prefix.include,
                '--shared-zlib-libpath=%s' % spec['zlib'].prefix.lib,
            ])

        if '+icu4c' in spec:
            options.extend(['--with-intl=full-icu'])
        # else:
        #     options.extend(['--with-intl=system-icu'])

        configure(*options)

        if self.run_tests:
            make('test')
            make('test-addons')

        if '+doc' in spec:
            make('doc')

        make('install')
