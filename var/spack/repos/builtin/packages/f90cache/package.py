# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class F90cache(AutotoolsPackage):
    """f90cache is a compiler cache. It acts as a caching pre-processor to
       Fortran compilers, using the -E compiler switch and a hash to detect
       when a compilation can be satisfied from cache. This often results in a
       great speedup in common compilations.
    """
    homepage = "https://perso.univ-rennes1.fr/edouard.canot/f90cache/"
    url      = "https://perso.univ-rennes1.fr/edouard.canot/f90cache/f90cache-0.99c.tar.gz"

    version('0.99c', sha256='13f8297ecba73671d43376b71ef0e453bd9d6677a901d1c95f01f16cc33776e1')
    version('0.99', 'e4767ae876203ed4f3e118e22204cdec',
            url='http://distfiles.exherbo.org/distfiles/f90cache-0.99.tar.bz2')
