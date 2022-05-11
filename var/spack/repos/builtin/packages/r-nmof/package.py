# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RNmof(RPackage):
    """Numerical Methods and Optimization in Finance.

    Functions, examples and data from the book "Numerical Methods and
    Optimization in Finance" by M. Gilli, D. Maringer and E. Schumann (2011),
    ISBN 978-0123756626. The package provides implementations of several
    optimisation heuristics, such as Differential Evolution, Genetic Algorithms
    and Threshold Accepting. There are also functions for the valuation of
    financial instruments, such as bonds and options, and functions that help
    with stochastic simulations."""

    cran = "NMOF"

    version('2.5-0', sha256='f44914c86d86c62f74cbc026179a694f0b3c2e3341b076acaf5de01de194a3c7')
    version('2.2-2', sha256='e64472f89023f0d779a35df753747d750174ce89644a9142312a1d2dc6f24642')
    version('1.6-0', sha256='5484cd43c28aaf23d560c2dde8bcd8dd440a205d2214eb50e02fe0bb42ec2755')

    depends_on('r@2.14:', type=('build', 'run'))
