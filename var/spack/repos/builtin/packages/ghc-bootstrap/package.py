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
import os

class GhcBootstrap(Package):
    """Install a binary package of the Glasgow Haskell Compiler
       that can be used to bootstrap a source package."""

    homepage = "https://www.haskell.org/ghc/"
    url      = "http://downloads.haskell.org/~ghc/8.0.1/ghc-8.0.1-x86_64-centos67-linux.tar.xz"

    version('8.0.1', '56b68669e0f7186f7624d2f7bd2c3c39')

    provides('haskell')
    # The CentOS 6-based package above needs this to run on CentOS 7.
    depends_on('gmp@4.3.2')

    def install(self, spec, prefix):
        # set LD_LIBRARY_PATH to use spack's libgmp.3.so
        os.environ['LD_LIBRARY_PATH'] = spec['gmp'].prefix.lib
        configure("--prefix=%s" % prefix)
        make("install")
