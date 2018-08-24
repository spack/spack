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


class Aida(Package):
    """Abstract Interfaces for Data Analysis"""

    homepage = "http://aida.freehep.org/"
    url      = "ftp://ftp.slac.stanford.edu/software/freehep/AIDA/v3.2.1/aida-3.2.1.tar.gz"

    version('3.2.1', sha256='c51da83e99c0985a7ef3e8bc5a60c3ae61f3ca603b61100c2438b4cdadd5bb2e')

    def install(self, spec, prefix):
        install_tree('src/cpp', prefix.include)
        install_tree('lib', prefix)
