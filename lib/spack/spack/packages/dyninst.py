##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
# 
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
# 
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *

class Dyninst(Package):
    homepage = "https://paradyn.org"
    url      = "http://www.dyninst.org/sites/default/files/downloads/dyninst/8.1.2/DyninstAPI-8.1.2.tgz"
    list_url = "http://www.dyninst.org/downloads/dyninst-8.x"

    versions = {'8.1.2' : 'bf03b33375afa66fe0efa46ce3f4b17a',
                '8.1.1' : '1f8743e3a5662b25ce64a7edf647e77d' }

    depends_on("libelf")
    depends_on("libdwarf")

    def install(self, spec, prefix):
        configure("--prefix=" + prefix)
        make()
        make("install")
