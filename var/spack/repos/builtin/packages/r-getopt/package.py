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


class RGetopt(RPackage):
    """Package designed to be used with Rscript to write "#!" shebang scripts
       that accept short and long flags/options. Many users will prefer using
       instead the packages optparse or argparse which add extra features like
       automatically generated help option and usage, support for default
       values, positional argument support, etc."""

    homepage = "https://github.com/trevorld/getopt"
    url      = "https://cran.r-project.org/src/contrib/getopt_1.20.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/getopt"

    version('1.20.1', '323cf2846e306f49236b8174bc3d4e47')
