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
from shutil import copytree


class StringViewLite(Package):
    """
    A single-file header-only version of a C++17-like string_view for C++98,
    C++11 and later
    """

    homepage = "https://github.com/martinmoene/string-view-lite"
    url      = "https://github.com/martinmoene/string-view-lite/archive/v1.0.0.tar.gz"

    version('1.0.0', sha256='44e30dedd6f4777e646da26528f9d2d5cc96fd0fa79e2e5c0adc14817d048d63')
    version('0.2.0', sha256='c8ae699dfd2ccd15c5835e9b1d246834135bbb91b82f7fc4211b8ac366bffd34')
    version('0.1.0', sha256='7de87d6595230a6085655dab6145340bc423f2cf206263ef73c9b78f7b153340')

    def install(self, spec, prefix):
        copytree('include', prefix.include)
