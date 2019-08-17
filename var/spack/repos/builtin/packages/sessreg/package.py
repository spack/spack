# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sessreg(AutotoolsPackage):
    """Sessreg is a simple program for managing utmp/wtmp entries for X
    sessions. It was originally written for use with xdm, but may also be
    used with other display managers such as gdm or kdm."""

    homepage = "http://cgit.freedesktop.org/xorg/app/sessreg"
    url      = "https://www.x.org/archive/individual/app/sessreg-1.1.0.tar.gz"

    version('1.1.0', '5d7eb499043c7fdd8d53c5ba43660312')

    depends_on('xproto@7.0.25:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')

    def patch(self):
        kwargs = {'string': True}
        filter_file('$(CPP) $(DEFS)', '$(CPP) -P $(DEFS)',
                    'man/Makefile.in', **kwargs)
