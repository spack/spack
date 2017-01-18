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


class Openjpeg(CMakePackage):
    """OpenJPEG is an open-source JPEG 2000 codec written in C language.

    It has been developed in order to promote the use of JPEG 2000, a
    still-image compression standard from the Joint Photographic
    Experts Group (JPEG).
    Since April 2015, it is officially recognized by ISO/IEC and
    ITU-T as a JPEG 2000 Reference Software.
    """

    homepage = "https://github.com/uclouvain/openjpeg"
    url = "https://github.com/uclouvain/openjpeg/archive/version.2.1.tar.gz"

    version('2.1',   '3e1c451c087f8462955426da38aa3b3d')
    version('2.0.1', '105876ed43ff7dbb2f90b41b5a43cfa5')
    version('2.0',   'cdf266530fee8af87454f15feb619609')
    version('1.5.2', '545f98923430369a6b046ef3632ef95c')
    version('1.5.1', 'd774e4b5a0db5f0f171c4fc0aabfa14e')

    def url_for_version(self, version):
        fmt = 'https://github.com/uclouvain/openjpeg/archive/version.{0}.tar.gz'
        return fmt.format(version.dotted)
