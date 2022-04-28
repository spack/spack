# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ScitokensCpp(CMakePackage):
    """ A C++ implementation of the SciTokens library with a C library interface.
        SciTokens provide a token format for distributed authorization. """

    homepage = "https://github.com/scitokens/scitokens-cpp"
    url      = "https://github.com/scitokens/scitokens-cpp/archive/refs/tags/v0.7.0.tar.gz"

    version('0.7.0', sha256='72600cf32523b115ec7abf4ac33fa369e0a655b3d3b390e1f68363e6c4e961b6')

    depends_on('sqlite')
    depends_on('curl')
    depends_on('uuid', type='build')

    # https://github.com/scitokens/scitokens-cpp/issues/72
    @when('^openssl@3:')
    def patch(self):
        filter_file(' -Werror', '', 'CMakeLists.txt')
