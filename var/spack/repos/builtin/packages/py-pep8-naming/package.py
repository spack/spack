# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPep8Naming(PythonPackage):
    """Check PEP-8 naming conventions, plugin for flake8."""

    homepage = "https://pypi.org/project/pep8-naming/"
    url      = "https://files.pythonhosted.org/packages/3e/4a/125425d6b1e017f48dfc9c961f4bb9510168db7a090618906c750184ed03/pep8-naming-0.7.0.tar.gz"

    extends('python', ignore='bin/(flake8|pyflakes|pycodestyle)')
    version('0.7.0', sha256='624258e0dd06ef32a9daf3c36cc925ff7314da7233209c5b01f7e5cdd3c34826')

    depends_on('py-flake8-polyfill', type='run')
