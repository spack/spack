# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMlxtend(PythonPackage):
    """Mlxtend (machine learning extensions) is a Python library of useful
       tools for the day-to-day data science tasks."""

    homepage = "http://rasbt.github.io/mlxtend/"
    url      = "https://github.com/rasbt/mlxtend/archive/v0.16.0.tar.gz"

    version('0.16.0', sha256='38789b36173630bf18e2244b035e7e6b44a87a0ae65cf04935cd2eecbf6595a1')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.16.2:', type=('build', 'run'))
    depends_on('py-scipy@1.2.1:', type=('build', 'run'))
    depends_on('py-pandas@0.24.2:', type=('build', 'run'))
    depends_on('py-scikit-learn@0.20.3:', type=('build', 'run'))
    depends_on('py-matplotlib@3.0.0:', type=('build', 'run'))
    depends_on('py-joblib@0.13.2:', type=('build', 'run'))
