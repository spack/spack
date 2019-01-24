# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys


class XercesC(AutotoolsPackage):
    """Xerces-C++ is a validating XML parser written in a portable subset of
    C++. Xerces-C++ makes it easy to give your application the ability to read
    and write XML data. A shared library is provided for parsing, generating,
    manipulating, and validating XML documents using the DOM, SAX, and SAX2
    APIs."""

    homepage = "https://xerces.apache.org/xerces-c"
    url      = "https://archive.apache.org/dist/xerces/c/3/sources/xerces-c-3.2.1.tar.bz2"

    version('3.2.2', '4c395216ecbef3c88a756ff4090e6f7e')
    version('3.2.1', '8f98a81a3589bbc2dad9837452f7d319')
    version('3.1.4', 'd04ae9d8b2dee2157c6db95fa908abfd')

    # It's best to be explicit about the transcoder or else xerces may
    # choose another value.
    if sys.platform == 'darwin':
        default_transcoder = 'macos'
    elif sys.platform.startswith('win') or sys.platform == 'cygwin':
        default_transcoder = 'windows'
    else:
        default_transcoder = 'gnuiconv'

    variant('transcoder', default=default_transcoder,
            values=('gnuiconv', 'iconv', 'icu', 'macos', 'windows'),
            multi=False,
            description='Use the specified transcoder')

    depends_on('libiconv', type='link', when='transcoder=gnuiconv')
    depends_on('icu4c',    type='link', when='transcoder=icu')

    # Pass flags to configure.  This is necessary for CXXFLAGS or else
    # the xerces default will override the spack wrapper.
    def flag_handler(self, name, flags):
        spec = self.spec

        # There is no --with-pkg for gnuiconv.
        if name == 'ldflags' and 'transcoder=gnuiconv' in spec:
            flags.append(spec['libiconv'].libs.ld_flags)

        return (None, None, flags)

    def configure_args(self):
        spec = self.spec
        args = ['--disable-network']

        if 'transcoder=gnuiconv' in spec:
            args.append('--enable-transcoder-gnuiconv')

        if 'transcoder=iconv' in spec:
            args.append('--enable-transcoder-iconv')

        if 'transcoder=icu' in spec:
            args.append('--enable-transcoder-icu')
            args.append('--with-icu=%s' % spec['icu4c'].prefix)

        if 'transcoder=macos' in spec:
            args.append('--enable-transcoder-macosunicodeconverter')

        if 'transcoder=windows' in spec:
            args.append('--enable-transcoder-windows')

        return args
