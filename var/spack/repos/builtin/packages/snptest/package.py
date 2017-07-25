##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
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


class Snptest(Package):
    """SNPTEST is a program for the analysis of single SNP association in
       genome-wide studies."""

    homepage = "https://mathgen.stats.ox.ac.uk/genetics_software/snptest/snptest.html"

    version('2.5.2', '', url='http://www.well.ox.ac.uk/~gav/resources/snptest_v2.5.2_linux_x86_64_dynamic.tgz', 
            when='platform=linux', preferred=True)
    version('2.5.2', '', url='http://www.well.ox.ac.uk/~gav/resources/snptest_v2.5.2_MacOSX_x86_64.tgz', when='platform=darwin')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('snptest_v2.5.2', prefix.bin)
