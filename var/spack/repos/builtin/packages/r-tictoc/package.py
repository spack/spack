# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTictoc(RPackage):
    """Functions for timing R scripts, as well as implementations of Stack and
    List structures.

    This package provides the timing functions 'tic' and 'toc' that can be
    nested. One can record all timings while a complex script is running, and
    examine the values later. It is also possible to instrument the timing
    calls with custom callbacks. In addition, this package provides class
    'Stack', implemented as a vector, and class 'List', implemented as a list,
    both of which support operations 'push', 'pop', 'first', 'last' and
    'clear'."""

    cran = "tictoc"

    version('1.0.1', sha256='a09a1535c417ddf6637bbbda5fca6edab6c7f7b252a64e57e99d4d0748712705')
    version('1.0', sha256='47da097c1822caa2d8e262381987cfa556ad901131eb96109752742526b2e2fe')

    depends_on('r@3.0.3:', type=('build', 'run'), when='@1.0.1:')
    depends_on('r@3.0.3:4.0', type=('build', 'run'), when='@1.0')
