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

class Git(Package):
    """Git is a free and open source distributed version control
       system designed to handle everything from small to very large
       projects with speed and efficiency."""
    homepage = "http://git-scm.com"
    url      = "https://github.com/git/git/tarball/v2.7.1"

    version('2.8.1', '1308448d95afa41a4135903f22262fc8')
    version('2.8.0', 'eca687e46e9750121638f258cff8317b')
    version('2.7.3', 'fa1c008b56618c355a32ba4a678305f6')
    version('2.7.1', 'bf0706b433a8dedd27a63a72f9a66060')


    # See here for info on vulnerable Git versions:
    # http://www.theregister.co.uk/2016/03/16/git_server_client_patch_now/
    # All the following are vulnerable
    #version('2.6.3', 'b711be7628a4a2c25f38d859ee81b423')
    #version('2.6.2', 'da293290da69f45a86a311ad3cd43dc8')
    #version('2.6.1', '4c62ee9c5991fe93d99cf2a6b68397fd')
    #version('2.6.0', 'eb76a07148d94802a1745d759716a57e')
    #version('2.5.4', '3eca2390cf1fa698b48e2a233563a76b')
    #version('2.2.1', 'ff41fdb094eed1ec430aed8ee9b9849c')


    depends_on("openssl")
    depends_on("autoconf")
    depends_on("curl")
    depends_on("expat")

    # Also depends_on gettext: apt-get install gettext (Ubuntu)

    # Use system perl for now.
    # depends_on("perl")
    # depends_on("pcre")

    depends_on("zlib")

    def install(self, spec, prefix):
        configure_args = [
            "--prefix=%s" % prefix,
            "--without-pcre",
            "--with-openssl=%s" % spec['openssl'].prefix,
            "--with-zlib=%s" % spec['zlib'].prefix,
            "--with-curl=%s" % spec['curl'].prefix,
            "--with-expat=%s" % spec['expat'].prefix,
            ]

        which('autoreconf')('-i')
        configure(*configure_args)
        make()
        make("install")
