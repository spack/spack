# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gccmakedep(AutotoolsPackage):
    """X.org gccmakedep utilities."""

    homepage = "https://cgit.freedesktop.org/xorg/util/gccmakedep/"
    url      = "https://www.x.org/archive/individual/util/gccmakedep-1.0.3.tar.gz"

    version('1.0.3', '127ddb6131eb4a56fdf6644a63ade788')

    depends_on('pkgconfig', type='build')
