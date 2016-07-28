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

class Wget(Package):
    """GNU Wget is a free software package for retrieving files using
       HTTP, HTTPS and FTP, the most widely-used Internet protocols. It
       is a non-interactive commandline tool, so it may easily be called
       from scripts, cron jobs, terminals without X-Windows support,
       etc."""

    homepage = "http://www.gnu.org/software/wget/"
    url      = "http://ftp.gnu.org/gnu/wget/wget-1.16.tar.gz"

    version('1.17', 'c4c4727766f24ac716936275014a0536')
    version('1.16', '293a37977c41b5522f781d3a3a078426')

    depends_on("openssl")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix,
                  "--with-ssl=openssl",
                  "OPENSSL_CFLAGS=-I%s" % spec['openssl'].prefix.include,
                  "OPENSSL_LIBS=-L%s -lssl -lcrypto -lz" % spec['openssl'].prefix.lib)
        make()
        make("install")
