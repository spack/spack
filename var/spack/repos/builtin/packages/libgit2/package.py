# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libgit2(CMakePackage):
    """libgit2 is a portable, pure C implementation of the Git core
    methods provided as a re-entrant linkable library with a solid
    API, allowing you to write native speed custom Git applications in
    any language which supports C bindings.
    """

    homepage = "https://libgit2.github.com/"
    url      = "https://github.com/libgit2/libgit2/archive/v0.24.2.tar.gz"

    version('0.26.0', '6ea75a8a5745a7b2a14d3ed94486e761')
    version('0.24.2', '735661b5b73e3c120d13e2bae21e49b3')

    depends_on('cmake@2.8:', type='build')
    depends_on('libssh2')
