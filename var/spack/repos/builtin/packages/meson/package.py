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


class Meson(PythonPackage):
    """Meson is a portable open source build system meant to be both
       extremely fast, and as user friendly as possible."""

    homepage = "http://mesonbuild.com/"
    url      = "https://github.com/mesonbuild/meson/archive/0.42.0.tar.gz"

    version('0.42.0', '9e26bf154ca439b78b1b9366c8a89437')
    version('0.41.2', 'aa9c69ced965e47f5c75a9257ee91ce3')
    version('0.41.1', 'c6d285b35cfd7acc8517124d417efbdc')

    variant('ninjabuild', default=True)

    depends_on('python@3:',        type=('build', 'run'))
    depends_on('ninja', when='+ninjabuild', type=('build', 'run'))
