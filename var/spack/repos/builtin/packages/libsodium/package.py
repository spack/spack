# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libsodium(AutotoolsPackage):
    """Sodium is a modern, easy-to-use software library for encryption,
    decryption, signatures, password hashing and more."""
    homepage = "https://download.libsodium.org/doc/"
    url      = "https://download.libsodium.org/libsodium/releases/libsodium-1.0.13.tar.gz"
    list_url = "https://download.libsodium.org/libsodium/releases/old"

    version('1.0.17', '0f71e2680187a1558b5461e6879342c5')
    version('1.0.16', '37b18839e57e7a62834231395c8e962b')
    version('1.0.15', '070373e73a0b10bd96f412e1732ebc42')
    version('1.0.13', 'f38aac160a4bd05f06f743863e54e499')
    version('1.0.12', 'c308e3faa724b630b86cc0aaf887a5d4')
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
            url += 'old/unsupported/'
        elif version < Version('1.0.16'):
            url += 'old/'
        return url + 'libsodium-{0}.tar.gz'.format(version)
