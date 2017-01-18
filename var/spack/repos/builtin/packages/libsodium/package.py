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


class Libsodium(AutotoolsPackage):
    """Sodium is a modern, easy-to-use software library for encryption,
    decryption, signatures, password hashing and more."""
    homepage = "https://download.libsodium.org/doc/"
    url      = "https://download.libsodium.org/libsodium/releases/libsodium-1.0.11.tar.gz"

    version('1.0.11', 'b58928d035064b2a46fb564937b83540')
    version('1.0.10', 'ea89dcbbda0b2b6ff6a1c476231870dd')
    version('1.0.3', 'b3bcc98e34d3250f55ae196822307fab')
    version('1.0.2', 'dc40eb23e293448c6fc908757738003f')
    version('1.0.1', '9a221b49fba7281ceaaf5e278d0f4430')
    version('1.0.0', '3093dabe4e038d09f0d150cef064b2f7')
    version('0.7.1', 'c224fe3923d1dcfe418c65c8a7246316')

    def url_for_version(self, version):
        url = 'https://download.libsodium.org/libsodium/releases/'
        if version < Version('1.0.4'):
            url += 'old/'
        return url + 'libsodium-{0}.tar.gz'.format(version)
