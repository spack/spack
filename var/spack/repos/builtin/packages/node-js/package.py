# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys
import subprocess


class NodeJs(Package):
    """Node.js is a JavaScript runtime built on Chrome's V8 JavaScript
    engine."""

    homepage = "https://nodejs.org/"
    url      = "https://nodejs.org/download/release/v6.3.0/node-v6.3.0.tar.gz"

    version('11.1.0',  sha256='3f53b5ac25b2d36ad538267083c0e603d9236867a936c22a9116d95fa10c60d5')
    version('10.13.0', sha256='aa06825fff375ece7c0d881ae0de5d402a857e8cabff9b4a50f2f0b7b44906be')
    version('8.9.1',   sha256='32491b7fcc4696b2cdead45c47e52ad16bbed8f78885d32e873952fee0f971e1')
    version('7.1.0',   sha256='595e7e2a37d1e0573044a90077bb12c0f750e5d8851899ffa74038238da9a983')
    version('6.3.0',   sha256='4ed7a99985f8afee337cc22d5fef61b495ab4238dfff3750ac9019e87fc6aae6')
    version('6.2.2',   sha256='b6baee57a0ede496c7c7765001f7495ad74c8dfe8c34f1a6fb2cd5d8d526ffce')

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
    depends_on('openssl@1.0.2d:1.0.99', when='@:9+openssl')
    depends_on('openssl@1.1:', when='@10:+openssl')
    depends_on('zlib', when='+zlib')

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
