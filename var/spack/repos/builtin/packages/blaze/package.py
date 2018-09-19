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


class Blaze(Package):
    """Blaze is an open-source, high-performance C++ math library for dense and
    sparse arithmetic. With its state-of-the-art Smart Expression Template
    implementation Blaze combines the elegance and ease of use of a
    domain-specific language with HPC-grade performance, making it one of the
    most intuitive and fastest C++ math libraries available.
    """

    homepage = "https://bitbucket.org/blaze-lib/blaze/overview"
    url      = "https://bitbucket.org/blaze-lib/blaze/downloads/blaze-3.1.tar.gz"

    version('3.2', '47bd4a4f1b6292f5a6f71ed9d5287480')
    version('3.1', '2938e015f0d274e8d62ee5c4c0c1e9f3')
    version('3.0', '0c4cefb0be7b5a27ed8a377941be1ab1')
    version('2.6', 'f7b515eeffd5cce92eb02dc6f8905f4d')
    version('2.5', '53a862763c275046ff0a8f07dfd3985b')
    version('2.4', '7cf2e963a73d3c95ced0f7eaa0ae3677')
    version('2.3', '2f8ca52d23447ac75a03bb43b12ef774')
    version('2.2', '686a514108d7f3c6c7325ed57c171a59')
    version('2.1', 'e5e419a2b35f0a36cd9d7527a250c56a')
    version('2.0', 'aeb6a865e9e3810ee55456f961458a8e')
    version('1.5', '5b77b605ee5ad35631bb3039737142c9')
    version('1.4', '3f06d710161954ccae0975d87f1069ca')
    version('1.3', 'ebd7f91fc5fca4108bfd16a86f9abd82')
    version('1.2', 'b1511324456c3f70fce198a2b63e71ef')
    version('1.1', '5e52ebe68217f2e50d66dfdb9803d51e')
    version('1.0', 'a46508a2965ace9d89ded30a386d9548')

    def install(self, spec, prefix):
        install_tree('blaze', join_path(prefix.include, 'blaze'))
