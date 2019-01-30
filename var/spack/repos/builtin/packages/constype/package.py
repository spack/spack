# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Constype(AutotoolsPackage):
    """constype prints on the standard output the Sun code for the type of
    display that the specified device is.

    It was originally written for SunOS, but has been ported to other
    SPARC OS'es and to Solaris on both SPARC & x86."""

    homepage = "http://cgit.freedesktop.org/xorg/app/constype"
    url      = "https://www.x.org/archive/individual/app/constype-1.0.4.tar.gz"

    version('1.0.4', '2333b9ac9fd32e58b05afa651c4590a3')

    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')
