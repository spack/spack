# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rendercheck(AutotoolsPackage):
    """rendercheck is a program to test a Render extension implementation
    against separate calculations of expected output."""

    homepage = "http://cgit.freedesktop.org/xorg/app/rendercheck"
    url      = "https://www.x.org/archive/individual/app/rendercheck-1.5.tar.gz"

    version('1.5', '92ddef6d01f02529521af103f9b9bf60')

    depends_on('libxrender')
    depends_on('libx11')

    depends_on('xproto@7.0.17:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
