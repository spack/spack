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
import glob


class Anaconda3(Package):
    """Anaconda is the leading open data science platform powered by Python.
    The open source version of Anaconda is a high performance distribution of
    Python and R and includes over 100 of the most popular Python, R and Scala
    packages for ata science. This package is for Python 3.6."""

    homepage = "https://www.continuum.io/"
    url      = "https://repo.continuum.io/archive/Anaconda3-4.3.0-Linux-x86_64.sh"

    version('4.3.0', 'dbe2e78adeca1923643be2ecaacd6227', expand=False)

    def url_for_version(self, version):
        return "https://repo.continuum.io/archive/Anaconda3-{0}-Linux-x86_64.sh".format(version)

    def install(self, spec, prefix):
        bash = which('bash')
        installer = glob.glob('Anaconda3-*.sh')[0]
        bash(installer, '-b', '-f', '-p', prefix)
