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
import sys
from spack import *


class Git(Package):
    """Git is a free and open source distributed version control
       system designed to handle everything from small to very large
       projects with speed and efficiency."""
    homepage = "http://git-scm.com"
    url      = "https://github.com/git/git/tarball/v2.7.1"

    version('2.11.1', '2cf960f19e56f27248816809ae896794')
    version('2.11.0', 'c63fb83b86431af96f8e9722ebb3ca01')
    version('2.9.3', 'b0edfc0f3cb046aec7ed68a4b7282a75')
    version('2.9.2', '3ff8a9b30fd5c99a02e6d6585ab543fc')
    version('2.9.1', 'a5d806743a992300b45f734d1667ddd2')
    version('2.9.0', 'bf33a13c2adc05bc9d654c415332bc65')
    version('2.8.4', '86afb10254c3803894c9863fb5896bb6')
    version('2.8.3', '0e19f31f96f9364fd247b8dc737dacfd')
    version('2.8.2', '3d55550880af98f6e35c7f1d7c5aecfe')
    version('2.8.1', '1308448d95afa41a4135903f22262fc8')
    version('2.8.0', 'eca687e46e9750121638f258cff8317b')
    version('2.7.3', 'fa1c008b56618c355a32ba4a678305f6')
    version('2.7.1', 'bf0706b433a8dedd27a63a72f9a66060')

    # See here for info on vulnerable Git versions:
    # http://www.theregister.co.uk/2016/03/16/git_server_client_patch_now/
    # All the following are vulnerable
    # version('2.6.3', 'b711be7628a4a2c25f38d859ee81b423')
    # version('2.6.2', 'da293290da69f45a86a311ad3cd43dc8')
    # version('2.6.1', '4c62ee9c5991fe93d99cf2a6b68397fd')
    # version('2.6.0', 'eb76a07148d94802a1745d759716a57e')
    # version('2.5.4', '3eca2390cf1fa698b48e2a233563a76b')
    # version('2.2.1', 'ff41fdb094eed1ec430aed8ee9b9849c')

    depends_on("autoconf", type='build')
    depends_on("curl")
    depends_on("expat")
    depends_on("gettext")
    depends_on("libiconv")
    depends_on("openssl")
    depends_on("pcre")
    depends_on("perl")
    depends_on("zlib")

    def install(self, spec, prefix):
        env['LDFLAGS'] = "-L%s" % spec['gettext'].prefix.lib + " -lintl"
        configure_args = [
            "--prefix=%s" % prefix,
            "--with-curl=%s" % spec['curl'].prefix,
            "--with-expat=%s" % spec['expat'].prefix,
            "--with-iconv=%s" % spec['libiconv'].prefix,
            "--with-libpcre=%s" % spec['pcre'].prefix,
            "--with-openssl=%s" % spec['openssl'].prefix,
            "--with-perl=%s" % join_path(spec['perl'].prefix.bin, 'perl'),
            "--with-zlib=%s" % spec['zlib'].prefix,
        ]

        which('autoreconf')('-i')
        configure(*configure_args)
        if sys.platform == "darwin":
            # Don't link with -lrt; the system has no (and needs no) librt
            filter_file(r' -lrt$', '', 'Makefile')
        make()
        make("install")
