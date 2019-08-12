# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LibpthreadStubs(AutotoolsPackage):
    """The libpthread-stubs package provides weak aliases for pthread
    functions not provided in libc or otherwise available by default."""

    homepage = "https://xcb.freedesktop.org/"
    url      = "https://xcb.freedesktop.org/dist/libpthread-stubs-0.4.tar.gz"

    version('0.4', '7d2734e604a3e2f6f665c420b835ab62')
    version('0.3', 'a09d928c4af54fe5436002345ef71138')
