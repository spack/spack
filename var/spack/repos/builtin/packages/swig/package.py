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


class Swig(AutotoolsPackage):
    """SWIG is an interface compiler that connects programs written in
       C and C++ with scripting languages such as Perl, Python, Ruby,
       and Tcl. It works by taking the declarations found in C/C++
       header files and using them to generate the wrapper code that
       scripting languages need to access the underlying C/C++
       code. In addition, SWIG provides a variety of customization
       features that let you tailor the wrapping process to suit your
       application."""

    homepage = "http://www.swig.org"
    url      = "http://prdownloads.sourceforge.net/swig/swig-3.0.12.tar.gz"

    version('3.0.12', '82133dfa7bba75ff9ad98a7046be687c')
    version('3.0.11', '13732eb0f1ab2123d180db8425c1edea')
    version('3.0.10', 'bb4ab8047159469add7d00910e203124')
    version('3.0.8',  'c96a1d5ecb13d38604d7e92148c73c97')
    version('3.0.2',  '62f9b0d010cef36a13a010dc530d0d41')
    version('2.0.12', 'c3fb0b2d710cc82ed0154b91e43085a4')
    version('2.0.2',  'eaf619a4169886923e5f828349504a29')
    version('1.3.40', '2df766c9e03e02811b1ab4bba1c7b9cc')

    depends_on('pcre')

    build_directory = 'spack-build'
