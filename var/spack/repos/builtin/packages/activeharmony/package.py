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


class Activeharmony(Package):
    """Active Harmony: a framework for auto-tuning (the automated search for
       values to improve the performance of a target application)."""
    homepage = "http://www.dyninst.org/harmony"
    url      = "http://www.dyninst.org/sites/default/files/downloads/harmony/ah-4.5.tar.gz"

    version('4.5', 'caee5b864716d376e2c25d739251b2a9')

    def install(self, spec, prefix):
        make("CFLAGS=-O3")
        make("install", 'PREFIX=%s' % prefix)
