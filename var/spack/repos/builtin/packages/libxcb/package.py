# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxcb(AutotoolsPackage):
    """The X protocol C-language Binding (XCB) is a replacement
    for Xlib featuring a small footprint, latency hiding, direct
    access to the protocol, improved threading support, and
    extensibility."""

    homepage = "https://xcb.freedesktop.org/"
    url      = "https://xcb.freedesktop.org/dist/libxcb-1.13.tar.gz"

    version('1.13',   '3ba7fe0a7d60650bfb73fbf623aa57cc')
    version('1.12',   '95eee7c28798e16ba5443f188b27a476')
    version('1.11.1', '118623c15a96b08622603a71d8789bf3')
    version('1.11',   '1698dd837d7e6e94d029dbe8b3a82deb')

    depends_on('libpthread-stubs')
    depends_on('libxau@0.99.2:')
    depends_on('libxdmcp')

    # libxcb 1.X requires xcb-proto >= 1.X
    depends_on('xcb-proto', type='build')
    depends_on('xcb-proto@1.13:', when='@1.13:1.13.999', type='build')
    depends_on('xcb-proto@1.12:', when='@1.12:1.12.999', type='build')
    depends_on('xcb-proto@1.11:', when='@1.11:1.11.999', type='build')

    # TODO: uncomment once build deps can be resolved separately
    # See #7646, #4145, #4063, and #2548 for details
    # libxcb 1.13 added Python 3 support
    # depends_on('python', type='build')
    # depends_on('python@2:2.8', when='@:1.12', type='build')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')

    def patch(self):
        filter_file(
            'typedef struct xcb_auth_info_t {',
            'typedef struct {',
            'src/xcb.h')
