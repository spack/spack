# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libvpx(AutotoolsPackage):
    """libvpx is a free software video codec library from Google and the
    Alliance for Open Media.
    It serves as the reference software implementation for the VP8 and VP9
    video coding formats, and for AV1 a special fork named libaom that was
    stripped of backwards compatibility.
    """

    homepage = "https://chromium.googlesource.com/webm/libvpx"
    url      = "https://github.com/webmproject/libvpx/archive/refs/tags/v1.10.0.tar.gz"

    version('1.10.0', sha256='85803ccbdbdd7a3b03d930187cb055f1353596969c1f92ebec2db839fa4f834a')

    variant('pic', default=True,
            description='Produce position-independent code (for shared libs)')

    depends_on('yasm')

    def configure_args(self):
        extra_args = []
        if "+pic" in self.spec:
            extra_args.append('--enable-pic')
        return extra_args
