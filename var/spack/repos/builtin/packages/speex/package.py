# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Speex(AutotoolsPackage):
    """Speex is an Open Source/Free Software patent-free
    audio compression format designed for speech."""

    homepage = "https://speex.org"
    url      = "http://downloads.us.xiph.org/releases/speex/speex-1.2.0.tar.gz"

    version('1.2.0', '8ab7bb2589110dfaf0ed7fa7757dc49c')
