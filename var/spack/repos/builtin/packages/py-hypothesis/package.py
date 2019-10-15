# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyHypothesis(PythonPackage):
    """A library for property based testing."""

    homepage = "https://github.com/HypothesisWorks/hypothesis-python"
    url      = "https://pypi.io/packages/source/h/hypothesis/hypothesis-3.7.0.tar.gz"

    import_modules = [
        'hypothesis', 'hypothesis.searchstrategy', 'hypothesis.extra',
        'hypothesis.tools', 'hypothesis.utils', 'hypothesis.vendor',
        'hypothesis.internal', 'hypothesis.internal.conjecture'
    ]

    # TODO: Add missing dependency required to import hypothesis.extra.django

    version('4.7.2',  sha256='87944c6379f77634474b88abbf1e5ed5fe966637cc926131eda5e2af5b54a608')
    version('3.7.0', sha256='0fea49d08f2d5884f014151a5af6fb48d862f6ad567ffc4a2e84abf2f186c423')

    depends_on('py-setuptools', type='build')
    depends_on('py-enum34', type=('build', 'run'), when='^python@:2')
