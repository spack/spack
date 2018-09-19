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


class Libxslt(AutotoolsPackage):
    """Libxslt is the XSLT C library developed for the GNOME
       project. XSLT itself is a an XML language to define
       transformation for XML. Libxslt is based on libxml2 the XML C
       library developed for the GNOME project. It also implements
       most of the EXSLT set of processor-portable extensions
       functions and some of Saxon's evaluate and expressions
       extensions."""
    homepage = "http://www.xmlsoft.org/XSLT/index.html"
    url      = "http://xmlsoft.org/sources/libxslt-1.1.28.tar.gz"

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
