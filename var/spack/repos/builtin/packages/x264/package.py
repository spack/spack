# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class X264(AutotoolsPackage):
    """Software library and application for encoding video streams"""

    homepage = "https://www.videolan.org/developers/x264.html"
    git     = "https://code.videolan.org/videolan/x264.git"

    version('r2984', commit='3759fcb7b48037a5169715ab89f80a0ab4801cdf')

    depends_on('nasm')

    def configure_args(self):
        return ['--enable-shared', '--enable-pic']
