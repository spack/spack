# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNestle(PythonPackage):
    """Nested sampling algorithms for evaluating Bayesian evidence."""

    homepage = "http://kbarbary.github.io/nestle/"
    url = "https://pypi.io/packages/source/n/nestle/nestle-0.1.1.tar.gz"

    version('0.1.1', '4875c0f9a0a8e263c1d7f5fa6ce604c5')

    # Required dependencies
    depends_on('py-numpy', type=('build', 'run'))

    # Optional dependencies
    depends_on('py-scipy', type=('build', 'run'))
