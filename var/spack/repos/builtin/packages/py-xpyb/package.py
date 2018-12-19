# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyXpyb(AutotoolsPackage):
    """xpyb provides a Python binding to the X Window System protocol
    via libxcb."""

    homepage = "https://xcb.freedesktop.org/"
    url      = "https://xcb.freedesktop.org/dist/xpyb-1.3.1.tar.gz"

    version('1.3.1', '75d567e25517fb883a56f10b77fd2757')

    extends('python')

    depends_on('libxcb@1.5:')

    depends_on('xcb-proto@1.7.1:', type='build')
