# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class XcbProto(AutotoolsPackage):
    """xcb-proto provides the XML-XCB protocol descriptions that libxcb uses to
    generate the majority of its code and API."""

    homepage = "http://xcb.freedesktop.org/"
    url      = "http://xcb.freedesktop.org/dist/xcb-proto-1.13.tar.gz"

    version('1.13', sha256='0698e8f596e4c0dbad71d3dc754d95eb0edbb42df5464e0f782621216fa33ba7')
    version('1.12', sha256='cfa49e65dd390233d560ce4476575e4b76e505a0e0bacdfb5ba6f8d0af53fd59')
    version('1.11', sha256='d12152193bd71aabbdbb97b029717ae6d5d0477ab239614e3d6193cc0385d906')

    # TODO: uncomment once build deps can be resolved separately
    # See #7646, #4145, #4063, and #2548 for details
    # extends('python')

    patch('xcb-proto-1.12-schema-1.patch', when='@1.12')
