# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTypesPyyaml(PythonPackage):
    """Typing stubs for PyYAML."""

    homepage = "https://github.com/python/typeshed"
    url      = "https://files.pythonhosted.org/packages/3c/96/22a02c905aec42d8f7f7c48b7a00d68019edd4768e3fb94b754966d07870/types-PyYAML-5.4.6.tar.gz"

    version('5.4.6', sha256='745dcb4b1522423026bcc83abb9925fba747f1e8602d902f71a4058f9e7fb662')

    depends_on('py-setuptools', type=('build'))
