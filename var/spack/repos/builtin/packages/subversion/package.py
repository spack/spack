# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Subversion(Package):
    """Apache Subversion - an open source version control system."""
    homepage = 'https://subversion.apache.org/'
    url = 'http://archive.apache.org/dist/subversion/subversion-1.8.13.tar.gz'

    version('1.9.7',     sha256='c72a209c883e20245f14c4e644803f50ae83ae24652e385ff5e82300a0d06c3c')
    version('1.9.6',     sha256='a400cbc46d05cb29f2d7806405bb539e9e045b24013b0f12f8f82688513321a7')
    version('1.9.5',     sha256='280ba586c5d51d7b976b65d22d5e8e42f3908ed1c968d71120dcf534ce857a83')
    version('1.9.3',     sha256='74cd21d2f8a2a54e4dbd2389fe1605a19dbda8ba88ffc4bb0edc9a66e143cc93')
    version('1.8.17',    sha256='1b2cb9a0ca454035e55b114ee91c6433b9ede6c2893f2fb140939094d33919e4')
    version('1.8.13',    sha256='17e8900a877ac9f0d5ef437c20df437fec4eb2c5cb9882609d2277e2312da52c')

    variant('perl', default=False, description='Build with Perl bindings')

    depends_on('apr')
    depends_on('apr-util')
    depends_on('zlib')
    depends_on('sqlite')
    depends_on('serf')

    extends('perl', when='+perl')
    depends_on('swig@1.3.24:3.0.0', when='+perl')
    depends_on('perl-term-readkey', when='+perl')

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

        if 'swig' in spec:
            options.append('--with-swig=%s' % spec['swig'].prefix)
        if 'perl' in spec:
            options.append('PERL=%s' % spec['perl'].command.path)

        configure(*options)
        make()
        if self.run_tests:
            make('check')
        make('install')

        if spec.satisfies('+perl'):
            make('swig-pl')
            if self.run_tests:
                make('check-swig-pl')
            make('install-swig-pl-lib')
            with working_dir(join_path(
                    'subversion', 'bindings', 'swig', 'perl', 'native')):
                perl = which('perl')
                perl('Makefile.PL', 'INSTALL_BASE=%s' % prefix)
                make('install')

        # python bindings
        # make('swig-py',
        #     'swig-pydir=/usr/lib/python2.7/site-packages/libsvn',
        #     'swig_pydir_extra=/usr/lib/python2.7/site-packages/svn')
        # make('install-swig-py',
        #     'swig-pydir=/usr/lib/python2.7/site-packages/libsvn',
        #     'swig_pydir_extra=/usr/lib/python2.7/site-packages/svn')

        # ruby bindings
        # make('swig-rb')
        # make('isntall-swig-rb')
