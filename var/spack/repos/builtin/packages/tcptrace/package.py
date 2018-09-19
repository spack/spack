##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
from os.path import join


class Tcptrace(AutotoolsPackage):
    """tcptrace is a tool written by Shawn Ostermann at Ohio University for
       analysis of TCP dump files. It can take as input the files produced by
       several popular packet-capture programs, including tcpdump, snoop,
       etherpeek, HP Net Metrix, and WinDump."""

    homepage = "http://www.tcptrace.org/"
    url      = "http://www.tcptrace.org/download/tcptrace-6.6.7.tar.gz"

    version('6.6.7', '68128dc1817b866475e2f048e158f5b9')

    depends_on('bison', type='build')
    depends_on('flex', type='build')
    depends_on('libpcap')

    # Fixes incorrect API access in libpcap.
    # See https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=545595
    patch('tcpdump.patch')

    @run_after('configure')
    def patch_makefile(self):
        # see https://github.com/blitz/tcptrace/blob/master/README.linux
        makefile = FileFilter('Makefile')
        makefile.filter(
            "PCAP_LDLIBS = -lpcap",
            "DEFINES += -D_BSD_SOURCE\nPCAP_LDLIBS = -lpcap")

    def install(self, spec, prefix):
        # The build system has trouble creating directories
        mkdirp(prefix.bin)
        install('tcptrace', join(prefix.bin, 'tcptrace'))
