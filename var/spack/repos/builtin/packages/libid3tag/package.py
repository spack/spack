# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Libid3tag(AutotoolsPackage):
    """library for id3 tagging"""

    homepage = "https://www.underbit.com/products/mad/"
    url      = "ftp://ftp.mars.org/pub/mpeg/libid3tag-0.15.1b.tar.gz"

    maintainers = ['TheQueasle']

    version('0.15.1b', 'e5808ad997ba32c498803822078748c3')

    depends_on('zlib')
    depends_on('gperf')

    patch('10_utf16.diff')
    patch('11_unknown_encoding.dif')
    patch('CVE-2008-2109.patch', level=0)
    patch('libid3tag-gperf.patch', when="^gperf@3.1:")

    @run_before('configure')
    def preclean(self):
        """
        Remove compat.c and frametype.c in order to regenerate from gperf sources
        """
        rm = which('rm')
        rm('-v', 'compat.c')
        rm('-v', 'frametype.c')
