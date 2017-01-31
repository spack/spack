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


class RStringi(RPackage):
    """Allows for fast, correct, consistent, portable, as well as convenient
    character string/text processing in every locale and any native encoding.
    Owing to the use of the ICU library, the package provides R users with
    platform-independent functions known to Java, Perl, Python, PHP, and Ruby
    programmers. Among available features there are: pattern searching (e.g.,
    with ICU Java-like regular expressions or the Unicode Collation Algorithm),
    random string generation, case mapping, string transliteration,
    concatenation, Unicode normalization, date-time formatting and parsing,
    etc."""

    homepage = "http://www.gagolewski.com/software/stringi/"
    url      = "https://cran.r-project.org/src/contrib/stringi_1.1.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/stringi"

    version('1.1.2', '0ec2faa62643e1900734c0eaf5096648')
    version('1.1.1', '32b919ee3fa8474530c4942962a6d8d9')

    depends_on('icu4c')
