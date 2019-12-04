# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install swipl
#
# You can edit this file again by typing:
#
#     spack edit swipl
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Swipl(CMakePackage):
    """ SWI-Prolog is a versatile implementation of the Prolog language.
    Although SWI-Prolog gained its popularity primarily in education,
    its development is mostly driven by the needs for application development.
    This is facilitated by a rich interface to other IT components by
    supporting many document types and (network) protocols as well as a
    comprehensive low-level interface to C that is the basis for high-level
    interfaces to C++, Java (bundled), C#, Python, etc (externally available).

    Data type extensions such as dicts and strings as well as full support
    for Unicode and unbounded integers simplify smooth exchange of data
    with other components."""

    homepage = "https://www.swi-prolog.org"
    url      = "https://www.swi-prolog.org/download/stable/src/swipl-8.0.3.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('8.0.3', sha256='cee59c0a477c8166d722703f6e52f962028f3ac43a5f41240ecb45dbdbe2d6ae')

    variant('gmp', default=True, description='bignum and rational number support')
    variant('xpce', default=True, description='GUI support')
    variant('ssl', default=True, description='SSL support')
    variant('zlib', default=True, description='Compressed streams support')
    variant('odbc', default=True, description='ODBC database access')
    variant('unwind', default=True, description='Build with stack traces in crash reports')

    depends_on('uuid')
    depends_on('readline')

    depends_on('gmp', when='+gmp')
    depends_on('unwind', when='+unwind')
    depends_on('unixodbc', when='+odbc')
    depends_on('openssl', when='+ssl')
    depends_on('zlib', when='+zlib')

    depends_on('libxt', when='+xpce')
    depends_on('libx11', when='+xpce')
    depends_on('libjpeg', when='+xpce')
    depends_on('libxpm', when='+xpce')

    depends_on('libxft', when='+xpce')
    depends_on('fontconfig', when='+xpce')
    depends_on('pkg-config', when='+xpce')

    def cmake_args(self):
        args = []

        def append_switch(variant, cmake_flag):
            val = 'ON' if variant in self.spec else 'OFF'
            args.append('-D{}:BOOL={}'.format(cmake_flag, val))

        append_switch('+gmp', 'USE_GMP')
        append_switch('+xpce', 'SWIPL_PACKAGES_X')
        append_switch('+odbc', 'SWIPL_PACKAGES_ODBC')

        # The variants ssl and zlib are implicitly set up by the build system

        return args
