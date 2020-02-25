# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyaml(PythonPackage):
    """PyYAML-based module to produce pretty and readable YAML-serialized
    data."""

    homepage = "https://github.com/mk-fg/pretty-yaml"
    url      = "https://pypi.io/packages/source/p/pyaml/pyaml-19.4.1.tar.gz"

    version('19.4.1', sha256='c79ae98ececda136a034115ca178ee8bf3aa7df236c488c2f55d12f177b88f1e')

    depends_on('py-setuptools', type=('build'))

    depends_on('py-pyyaml', type='run')
