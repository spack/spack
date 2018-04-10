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


class CLime(AutotoolsPackage):
    """LIME (which can stand for Lattice QCD Interchange Message Encapsulation
       or more generally, Large Internet Message Encapsulation) is a simple
       packaging scheme for combining records containing ASCII and/or binary
       data."""

    homepage = "https://usqcd-software.github.io/c-lime/"
    url      = "https://github.com/usqcd-software/c-lime/archive/qio2-3-9.tar.gz"

    version('2-3-9', '28257e7ae75dc68c7c920e3e16db0ec9')
