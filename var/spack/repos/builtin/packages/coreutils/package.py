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


class Coreutils(AutotoolsPackage):
    """The GNU Core Utilities are the basic file, shell and text
       manipulation utilities of the GNU operating system.  These are
       the core utilities which are expected to exist on every
       operating system.
    """
    homepage = "http://www.gnu.org/software/coreutils/"
    url      = "https://ftpmirror.gnu.org/coreutils/coreutils-8.26.tar.xz"

    version('8.29', '960cfe75a42c9907c71439f8eb436303')
    version('8.26', 'd5aa2072f662d4118b9f4c63b94601a6')
    version('8.23', 'abed135279f87ad6762ce57ff6d89c41')

    build_directory = 'spack-build'
