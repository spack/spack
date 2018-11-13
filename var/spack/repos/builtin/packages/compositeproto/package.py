# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Compositeproto(AutotoolsPackage):
    """Composite Extension.

    This package contains header files and documentation for the composite
    extension.  Library and server implementations are separate."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/compositeproto"
    url      = "https://www.x.org/archive/individual/proto/compositeproto-0.4.2.tar.gz"

    version('0.4.2', '2dea7c339432b3363faf2d29c208e7b5')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
