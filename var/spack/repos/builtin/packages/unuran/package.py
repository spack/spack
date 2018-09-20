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


class Unuran(AutotoolsPackage):
    """Universal Non-Uniform Random number generator."""

    homepage = "http://statmath.wu.ac.at/unuran"
    url      = "http://statmath.wu.ac.at/unuran/unuran-1.8.1.tar.gz"

    version('1.8.1', 'a5885baab53a2608c1d85517bf5d06a5')

    variant('shared', default=True,
        description="Enable the build of shared libraries")
    variant('rngstreams', default=True,
        description="Use RNGSTREAM library for uniform random generation")
    variant('gsl',      default=False,
        description="Use random number generators from GNU Scientific Library")

    depends_on('gsl',        when="+gsl")
    depends_on('rngstreams', when="+rngstreams")

    def configure_args(self):

        spec = self.spec

        args = [
            '--%s-shared' % ('enable' if '+shared' in spec else 'disable'),
            '--with-urgn-default=%s' % (
                'rngstream' if '+rngstreams' in spec else 'builtin'),
            '--%s-urng-gsl' % (
                'with' if '+gsl' in spec else 'without'),
            '--%s-urng-rngstreams' % (
                'with' if '+rngstreams' in spec else 'without')
        ]

        return args
