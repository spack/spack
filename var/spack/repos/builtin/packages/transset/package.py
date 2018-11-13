# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Transset(AutotoolsPackage):
    """transset is an utility for setting opacity property."""

    homepage = "http://cgit.freedesktop.org/xorg/app/transset"
    url      = "https://www.x.org/archive/individual/app/transset-1.0.1.tar.gz"

    version('1.0.1', '4bbee6f6ea6fbd403280b4bb311db6dc')

    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
