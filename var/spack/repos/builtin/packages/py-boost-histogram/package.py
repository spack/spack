# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyBoostHistogram(PythonPackage):
    """The Boost::Histogram Python wrapper."""

    homepage = "https://github.com/scikit-hep/boost-histogram"
    pypi     = "boost_histogram/boost_histogram-1.2.1.tar.gz"

    version('1.2.1', sha256='a27842b2f1cfecc509382da2b25b03056354696482b38ec3c0220af0fc9b7579')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools@45:', type='build')
    depends_on('py-setuptools-scm@4.1.2:+toml', type='build')
    depends_on('py-numpy@1.13.3:', type=('build', 'run'))
    depends_on('py-dataclasses', type=('build', 'run'), when='^python@:3.6')
    depends_on('py-typing-extensions', type=('build', 'run'), when='^python@:3.7')
