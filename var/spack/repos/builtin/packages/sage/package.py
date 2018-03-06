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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install sage
#
# You can edit this file again by typing:
#
#     spack edit sage
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class Sage(AutotoolsPackage):
    """SageMath is a free open-source mathematics software system licensed 
    under the GPL. It builds on top of many existing open-source packages: 
    NumPy, SciPy, matplotlib, Sympy, Maxima, GAP, FLINT, R and many more. 
    Access their combined power through a common, Python-based language or 
    directly via interfaces or wrappers."""

    homepage = "http://www.sagemath.org/"
    url      = "http://files.sagemath.org/src/sage-8.1.tar.gz"

    version('8.1', '66434fbd76a89e6b5abc3ad18feffeb0')

    # http://files.sagemath.org/src/README.txt
    # http://doc.sagemath.org/html/en/installation/source.html
    # gcc (w/ fortran), make, m4, perl, perl-extutils-makemaker, ranlib, openssl
    depends_on('gcc')
    depends_on('m4')
    depends_on('perl')
    depends_on('perl-extutils-makemaker')
    depends_on('binutils')
    depends_on('openssl')
    # optional...
    depends_on('texlive')
    depends_on('tk')
    depends_on('image-magick')
    depends_on('ffmpeg')
    #depends_on('dvipng')

    def configure_args(self):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
