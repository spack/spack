# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Bertini(AutotoolsPackage):
    """Bertini is a general-purpose solver, written in C, that was created
    for research about polynomial continuation. It solves for the numerical
    solution of systems of polynomial equations using homotopy continuation."""

    homepage = "https://bertini.nd.edu/"
    url      = "https://bertini.nd.edu/BertiniSource_v1.5.tar.gz"

    version('1.5', 'e3f6cc6e7f9a0cf1d73185e8671af707')

    variant('mpi', default=True, description='Compile in parallel')

    depends_on('flex', type='build')
    depends_on('bison', type='build')
    depends_on('gmp')
    depends_on('mpfr')
    depends_on('mpi', when='+mpi')
