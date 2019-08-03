# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: MIT
#
# ----------------------------------------------------------------------------
#
#     spack install sixs
#
# You can edit this file again by typing:
#
#     spack edit sixs
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Sixs(Package):
    """The 6S code is a basic RT code used for calculation of lookup
       tables in the MODIS atmospheric correction algorithm.
       It enables accurate simulations of satellite and plane observation,
       accounting for elevated targets, use of anisotropic and lambertian surfaces
       and calculation of gaseous absorption. 6S website is http://6s.ltdri.org."""

    homepage = "http://6s.ltdri.org"
    url      = "https://bitbucket.org/petebunting/6s/downloads/sixs-1.1.1.tar.gz"

    version('1.1.1', 'c294c46eaabe7d2685c2a6a430d92a70')
    
    parallel = False

    # Add dependencies if required.
    depends_on('cmake', type='build')
    
    def install(self, spec, prefix):    
        import subprocess
        cmd = 'cmake -DCMAKE_INSTALL_PREFIX='+str(prefix) + ' . '
        subprocess.call(cmd, shell=True)
        
        make()
        make('install')


