# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xproto(AutotoolsPackage):
    """X Window System Core Protocol.

    This package provides the headers and specification documents defining
    the X Window System Core Protocol, Version 11.

    It also includes a number of headers that aren't purely protocol related,
    but are depended upon by many other X Window System packages to provide
    common definitions and porting layer."""

    homepage = "http://cgit.freedesktop.org/xorg/proto/x11proto"
    url      = "https://www.x.org/archive/individual/proto/xproto-7.0.31.tar.gz"

    version('7.0.31', '04b925bf9e472c80f9212615cd684f1e')
    version('7.0.29', '16a78dd2c5ad73011105c96235f6a0af')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')

    def install(self, spec, prefix):
        # Installation fails in parallel
        # See https://github.com/spack/spack/issues/4805
        make('install', parallel=False)
