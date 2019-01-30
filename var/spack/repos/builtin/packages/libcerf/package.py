# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


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
