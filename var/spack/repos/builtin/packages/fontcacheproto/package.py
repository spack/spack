# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fontcacheproto(AutotoolsPackage):
    """X.org FontcacheProto protocol headers."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/fontcacheproto"
    url      = "https://www.x.org/archive/individual/proto/fontcacheproto-0.1.3.tar.gz"

    version('0.1.3', sha256='759b4863b55a25bfc8f977d8ed969da0b99b3c823f33c674d6da5825f9df9a79')
