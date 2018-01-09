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
<<<<<<< HEAD
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install ctffind
#
# You can edit this file again by typing:
#
#     spack edit ctffind
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
=======
>>>>>>> ffd435bad70bc3005e2d5b81e0119fa67c60db05
from spack import *


class Ctffind(AutotoolsPackage):
    """Fast and accurate defocus estimation from electron micrographs."""

    homepage = "http://grigoriefflab.janelia.org/ctffind4"
    url      = "http://grigoriefflab.janelia.org/sites/default/files/ctffind-4.1.8.tar.gz"

    version('4.1.8', '8ae9d9abe363141a3792981b5a2fae94')

    depends_on('wx')
    depends_on('fftw@3:')
