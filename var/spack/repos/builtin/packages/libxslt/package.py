# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxslt(AutotoolsPackage):
    """Libxslt is the XSLT C library developed for the GNOME project. XSLT
    itself is a an XML language to define transformation for XML. Libxslt is
    based on libxml2 the XML C library developed for the GNOME project. It also
    implements most of the EXSLT set of processor-portable extensions functions
    and some of Saxon's evaluate and expressions extensions."""

    homepage = "http://www.xmlsoft.org/XSLT/index.html"
    url      = "http://xmlsoft.org/sources/libxslt-1.1.32.tar.gz"

    version('1.1.32', sha256='526ecd0abaf4a7789041622c3950c0e7f2c4c8835471515fd77eec684a355460')
    version('1.1.29', 'a129d3c44c022de3b9dcf6d6f288d72e')
    version('1.1.28', '9667bf6f9310b957254fdcf6596600b7')
    version('1.1.26', 'e61d0364a30146aaa3001296f853b2b9')

    variant('crypto',  default=True,
            description='Build libexslt with crypto support')

    depends_on("libiconv")
    depends_on("libxml2")
    depends_on("xz")
    depends_on("zlib")
    depends_on("libgcrypt", when="+crypto")

    def configure_args(self):
        args = []
        if '~crypto' in self.spec:
            args.append('--without-crypto')
        else:
            args.append('--with-crypto')
        return args
