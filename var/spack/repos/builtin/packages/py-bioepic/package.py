# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBioepic(PythonPackage):
    """Diffuse domain ChIP-Seq caller based on SICER."""

    homepage = "https://github.com/biocore-ntnu/epic"
    git      = "https://github.com/biocore-ntnu/epic"
    url      = "https://pypi.io/packages/source/b/bioepic/bioepic-0.2.12.tar.gz"

    version('develop', branch='master', git=git)
    version('0.2.12', 'aa97bc47449b8491121d447161ad5542')

    # Also submitted upstream but no new releases are expected
    patch('Remove-coveralls-dependency.patch', when='@:0.2.12')

    depends_on('jellyfish@2:', type='run')
    depends_on('py-cython')
    depends_on('py-functools32', when='^python@2:2.999')
    depends_on('py-joblib')
    depends_on('py-natsort')
    depends_on('py-numpy')
    depends_on('py-pandas@0.23.0:')
    depends_on('py-pyfaidx')
    depends_on('py-scipy')
    depends_on('py-setuptools', type='build')
    depends_on('py-typing')
