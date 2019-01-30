# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libogg(AutotoolsPackage):
    """Ogg is a multimedia container format, and the native file and stream
    format for the Xiph.org multimedia codecs."""

    homepage = "https://www.xiph.org/ogg/"
    url      = "http://downloads.xiph.org/releases/ogg/libogg-1.3.2.tar.gz"

    version('1.3.2', 'b72e1a1dbadff3248e4ed62a4177e937')
