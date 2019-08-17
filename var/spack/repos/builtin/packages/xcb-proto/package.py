# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class XcbProto(AutotoolsPackage):
    """xcb-proto provides the XML-XCB protocol descriptions that libxcb uses to
    generate the majority of its code and API."""

    homepage = "http://xcb.freedesktop.org/"
    url      = "http://xcb.freedesktop.org/dist/xcb-proto-1.13.tar.gz"

    version('1.13', '0cc0294eb97e4af3a743e470e6a9d910')
    version('1.12', '5ee1ec124ea8d56bd9e83b8e9e0b84c4')
    version('1.11', 'c8c6cb72c84f58270f4db1f39607f66a')

    # TODO: uncomment once build deps can be resolved separately
    # See #7646, #4145, #4063, and #2548 for details
    # extends('python')

    patch('xcb-proto-1.12-schema-1.patch', when='@1.12')
