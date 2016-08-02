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


class CabalInstall(Package):
    """The 'cabal' command-line program simplifies the process of managing
       Haskell software by automating the fetching, configuration,
       compilation and installation of Haskell libraries and programs."""

    homepage = "http://www.haskell.org/cabal/"
    url      = "http://hackage.haskell.org/package/cabal-install-1.24.0.0/cabal-install-1.24.0.0.tar.gz"

    version('1.24.0.0', 'beb998cdc385523935620381abe393f4')

    depends_on('zlib')
    depends_on('ghc')

    # @mvkorpel's fix from:
    # https://github.com/haskell/cabal/issues/3440
    # It works around problem deciding whether to use collect2 or ld.
    # The symptom is complaint about "Setup: Unrecognized flags:..."
    patch('bootstrap.patch')

    def install(self, spec, prefix):
        bash=which("bash")
        bash("bootstrap.sh", "--sandbox", prefix)
        #bin.install ".cabal-sandbox/bin/cabal"
        #bash_completion.install "bash-completion/cabal"
