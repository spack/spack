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


class Cups(AutotoolsPackage):
    """CUPS is the standards-based, open source printing system developed by
    Apple Inc. for macOS and other UNIX-like operating systems. CUPS uses the
    Internet Printing Protocol (IPP) to support printing to local and network
    printers. This provides the core CUPS libraries, not a complete CUPS
    install."""

    homepage = "https://www.cups.org/"
    url = "https://github.com/apple/cups/releases/download/v2.2.3/cups-2.2.3-source.tar.gz"

    version('2.2.3', '006a8156680a516e43c59034e31df8bf')

    depends_on('gnutls')

    def configure_args(self):
        args = ['--enable-gnutls', '--with-components=core']
        return args
