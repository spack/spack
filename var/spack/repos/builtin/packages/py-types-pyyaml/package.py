# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTypesPyyaml(PythonPackage):
    """Typing stubs for PyYAML."""

    homepage = "https://github.com/python/typeshed"
    url      = "https://pypi.io/packages/source/t/types-pyyaml/types-PyYAML-5.4.6.tar.gz"

    version('5.4.6', sha256='745dcb4b1522423026bcc83abb9925fba747f1e8602d902f71a4058f9e7fb662')

    depends_on('py-setuptools', type=('build'))
