# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxpresent(AutotoolsPackage):
    """This package contains header files and documentation for the Present
    extension.  Library and server implementations are separate."""

    homepage = "https://cgit.freedesktop.org/xorg/lib/libXpresent/"
    url      = "https://www.x.org/archive/individual/lib/libXpresent-1.0.0.tar.gz"

    version('1.0.0', sha256='92f1bdfb67ae2ffcdb25ad72c02cac5e4912dc9bc792858240df1d7f105946fa')

    depends_on('libx11')

    depends_on('xproto', type='build')
    depends_on('presentproto@1.0:', type='build')
    depends_on('xextproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
