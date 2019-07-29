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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install sixs
#
# You can edit this file again by typing:
#
#     spack edit sixs
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *
import subprocess

class Sixs(Package):
    """The 6S code is a basic RT code used for calculation of lookup
       tables in the MODIS atmospheric correction algorithm.
       It enables accurate simulations of satellite and plane observation,
       accounting for elevated targets, use of anisotropic and lambertian surfaces
       and calculation of gaseous absorption. 6S website is http://6s.ltdri.org."""

    homepage = "http://6s.ltdri.org"
    url      = "https://bitbucket.org/petebunting/6s/downloads/sixs-1.1.1.tar.gz"

    version('1.1.2', '0ecc94dfc4ecf85461ae5836b0215d87')
    version('1.1.1', 'c294c46eaabe7d2685c2a6a430d92a70')
    
    parallel = False

    # Add dependencies if required.
    depends_on('cmake', type='build')
    
    def install(self, spec, prefix):    
        
        cmd = 'cmake -DCMAKE_INSTALL_PREFIX='+str(prefix) + ' . '
        subprocess.call(cmd, shell=True)
        
        make()
        make('install')


