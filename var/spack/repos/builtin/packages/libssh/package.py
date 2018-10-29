# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libssh(CMakePackage):
    """libssh: the SSH library"""

    homepage = "https://www.libssh.org"
    url      = "https://red.libssh.org/attachments/download/218/libssh-0.7.5.tar.xz"

    version('0.7.5', 'd3fc864208bf607ad87cdee836894feb')

    depends_on('openssl')
    depends_on('zlib')
