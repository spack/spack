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


class Glibc(AutotoolsPackage):
    """The GNU C Library is the standard system C library for all GNU systems,
    and is an important part of what makes up a GNU system.  It provides the
    system API for all programs written in C and C-compatible languages such
    as C++ and Objective C; the runtime facilities of other programming
    languages use the C library to access the underlying operating system."""

    homepage = "https://www.gnu.org/software/libc/"
    url      = "http://open-source-box.org/glibc/glibc-2.25.tar.gz"

    # Requires kernel headers from Linux 3.2.0+
    version('2.25',   '0c9f827298841dbf3bff3060f3d7f19c')

    # Works with kernel headers provided on CentOS 6
    version('2.16.0', 'b5f786fa7df4ff947bcd240c0e595f98')
    version('2.12.2', '49a8a5a74b624dcd15ec1689ede7e062')

    depends_on('binutils@2.22:')

    # TODO: Add a 'test' deptype
    # depends_on('python@2.7.6:2.8,3.4.3:', type='test')
    # depends_on('py-pexpect@4.0', type='test')
    # depends_on('gdb@7.8:', type='test')

    build_directory = 'spack-build'
