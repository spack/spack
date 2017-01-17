##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class Lzma(AutotoolsPackage):
    """LZMA Utils are legacy data compression software with high compression
    ratio. LZMA Utils are no longer developed, although critical bugs may be
    fixed as long as fixing them doesn't require huge changes to the code.

    Users of LZMA Utils should move to XZ Utils. XZ Utils support the legacy
    .lzma format used by LZMA Utils, and can also emulate the command line
    tools of LZMA Utils. This should make transition from LZMA Utils to XZ
    Utils relatively easy."""

    homepage = "http://tukaani.org/lzma/"
    url      = "http://tukaani.org/lzma/lzma-4.32.7.tar.gz"

    version('4.32.7', '2a748b77a2f8c3cbc322dbd0b4c9d06a')
