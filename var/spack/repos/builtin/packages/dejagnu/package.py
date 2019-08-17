# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dejagnu(AutotoolsPackage):
    """DejaGnu is a framework for testing other programs. Its purpose
    is to provide a single front end for all tests."""

    homepage = "https://www.gnu.org/software/dejagnu/"
    url      = "https://ftpmirror.gnu.org/dejagnu/dejagnu-1.6.tar.gz"

    version('1.6',   '1fdc2eb0d592c4f89d82d24dfdf02f0b')
    version('1.4.4', '053f18fd5d00873de365413cab17a666')

    depends_on('expect')
    depends_on('tcl@8.5:')

    # DejaGnu 1.4.4 cannot be built in parallel
    # `make check` also fails but this can be ignored
    parallel = False
