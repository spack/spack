# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lndir(AutotoolsPackage):
    """lndir - create a shadow directory of symbolic links to another
    directory tree."""

    homepage = "http://cgit.freedesktop.org/xorg/util/lndir"
    url      = "https://www.x.org/archive/individual/util/lndir-1.0.3.tar.gz"

    version('1.0.3', '7173b2e4832658d319c2980a7c834205')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
