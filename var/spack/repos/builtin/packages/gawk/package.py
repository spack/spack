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


class Gawk(AutotoolsPackage):
    """If you are like many computer users, you would frequently like to make
       changes in various text files wherever certain patterns appear, or
       extract data from parts of certain lines while discarding the
       rest. To write a program to do this in a language such as C or
       Pascal is a time-consuming inconvenience that may take many lines
       of code. The job is easy with awk, especially the GNU
       implementation: gawk.

       The awk utility interprets a special-purpose programming language
       that makes it possible to handle simple data-reformatting jobs
       with just a few lines of code.
    """

    homepage = "https://www.gnu.org/software/gawk/"
    url      = "http://ftp.gnu.org/gnu/gawk/gawk-4.1.4.tar.xz"

    version('4.1.4', '4e7dbc81163e60fd4f0b52496e7542c9')

    depends_on('gettext')
    depends_on('libsigsegv')
    depends_on('readline')
    depends_on('mpfr')
    depends_on('gmp')

    provides('awk')

    build_directory = 'spack-build'
