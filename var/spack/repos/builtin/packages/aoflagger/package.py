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


class Aoflagger(CMakePackage):
    """RFI detector and quality analysis for astronomical radio observations."""

    homepage = "https://sourceforge.net/projects/aoflagger/"
    url      = "https://downloads.sourceforge.net/project/aoflagger/aoflagger-2.10.0/aoflagger-2.10.0.tar.bz2"

    version('2.10.0', 'f1df6f9cc3ea87a529a3a53da9bb3033')

    depends_on('casacore+python+fftw@1.9.99:')
    depends_on('fftw~mpi@3.0:')
    depends_on('boost+python@:1.66.99')
    depends_on('libxml2')
    depends_on('lapack')
    depends_on('cfitsio')
