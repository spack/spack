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


class Libcerf(AutotoolsPackage):
    """A self-contained C library providing complex error functions, based
       on Faddeeva's plasma dispersion function w(z). Also provides Dawson's
       integral and Voigt's convolution of a Gaussian and a Lorentzian

    """
    homepage = "http://sourceforge.net/projects/libcerf"
    url      = "http://downloads.sourceforge.net/project/libcerf/libcerf-1.3.tgz"

    version('1.3', 'b3504c467204df71e62aeccf73a25612')

    def configure_args(self):
        spec = self.spec
        options = []
        # Clang reports unused functions as errors, see
        # http://clang.debian.net/status.php?version=3.8.1&key=UNUSED_FUNCTION
        if spec.satisfies('%clang'):
            options.append('CFLAGS=-Wno-unused-function')

        return options
