##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
from distutils.dir_util import copy_tree


class Dotkit(Package):
    """A set of shell scripts to help you setup, modify, and maintain a working
       Unix environment."""

    homepage = "https://sourceforge.net/projects/dotkit/"
    url      = "https://downloads.sourceforge.net/project/dotkit/dotkit/dotkit080521/dotkit080521.tar.gz?r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Fdotkit%2F&ts=1508871919&use_mirror=ayera"

    version('080521', '3e8b8bb37082214927443ebd27d3dab4')

    def install(self, spec, prefix):
        copy_tree(".", prefix, preserve_symlinks=1)
