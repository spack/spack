# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libzip(AutotoolsPackage):
    """libzip is a C library for reading, creating,
    and modifying zip archives."""

    homepage = "https://nih.at/libzip/index.html"
    url      = "https://nih.at/libzip/libzip-1.2.0.tar.gz"

    version('1.7.3', sha256='0e2276c550c5a310d4ebf3a2c3dfc43fb3b4602a072ff625842ad4f3238cb9cc')
    version('1.2.0', sha256='6cf9840e427db96ebf3936665430bab204c9ebbd0120c326459077ed9c907d9f')

    depends_on('zlib@1.1.2:')
