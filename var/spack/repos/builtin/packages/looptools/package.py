# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Looptools(AutotoolsPackage):
    """LoopTools is a package for evaluation of scalar and tensor one-loop
       integrals based on the FF package by G.J. van Oldenborgh. It
       features an easy Fortran, C++, and Mathematica interface to the
       scalar one-loop functions of FF and in addition provides
       the 2-, 3-, and 4-point tensor coefficient functions. """

    homepage = "http://www.feynarts.de/looptools/"
    url      = "http://www.feynarts.de/looptools/LoopTools-2.15.tar.gz"

    version('2.15', sha256='a065ffdc4fe6882aa3bb926134ba8ec875d6c0a633c3d4aa5f70db26542713f2')

    def configure_args(self):
        args = ["FFLAGS=-fPIC", "CFLAGS=-fPIC"]
        return args
