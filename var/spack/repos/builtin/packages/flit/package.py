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


class Flit(MakefilePackage):
    """Floating-point Litmus Tests (FLiT) is a C++ test infrastructure for
    detecting variability in floating-point code caused by variations in
    compiler code generation, hardware and execution environments."""

    homepage = "https://pruners.github.io/flit"
    url      = "https://github.com/PRUNERS/FLiT"
    url      = "https://github.com/PRUNERS/FLiT/archive/v2.0-alpha.1.tar.gz"

    version('2.0-alpha.1', '62cf7784bcdc15b962c813b11e478159')
    # FIXME: fix install and build to handle the old version, which is not
    #        installable
    # version('1.0.0',       '27763c89b044c5e3cfe62dd319a36a2b')
    conflicts("@:1.999", msg="Only can build version 2.0 and up")

    # Add dependencies
    depends_on('python@3:', type='run')
    depends_on('py-numpy', type='run')
    depends_on('py-matplotlib tk=False', type='run')
    depends_on('py-toml', type='run')

    @property
    def install_targets(self):
        return ['install', 'PREFIX=%s' % self.prefix]
