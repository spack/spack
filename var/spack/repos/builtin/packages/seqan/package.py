##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
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


class Seqan(CMakePackage):
    """SeqAn is an open source C++ library of efficient algorithms and data
    structures for the analysis of sequences with the focus on biological data.
    Our library applies a unique generic design that guarantees high
    performance, generality, extensibility, and integration with other
    libraries. SeqAn is easy to use and simplifies the development of new
    software tools with a minimal loss of performance"""

    homepage = "https://www.seqan.de"
    url      = "https://github.com/seqan/seqan/archive/seqan-v2.4.0.tar.gz"

    version('2.4.0rc2', 'bd62772b3661bf07dad2bf8f69a1bdaf')

    #depends on C++14 compiler: gcc >= 5, Clang/LLVM >= 3.6, Icc >= 17
    depends_on('cmake@3.4.0:', type='build')
    depends_on('python@2.7.0:', type='build')
    depends_on('py-nose')
    depends_on('py-sphinx')
    depends_on('boost')
    depends_on('zlib')
    depends_on('bzip2')
