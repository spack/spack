# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
    url      = "https://github.com/libgit2/libgit2/archive/v0.26.0.tar.gz"

    version('0.28.2', sha256='42b5f1e9b9159d66d86fff0394215c5733b6ef8f9b9d054cdd8c73ad47177fc3')
    version('0.26.0', sha256='6a62393e0ceb37d02fe0d5707713f504e7acac9006ef33da1e88960bd78b6eac')

    depends_on('cmake@2.8:', type='build')
    depends_on('libssh2')
