# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyTomli(PythonPackage):
    """Tomli is a Python library for parsing TOML.

    Tomli is fully compatible with TOML v1.0.0."""

    homepage = "https://github.com/hukkin/tomli"
    url = "https://files.pythonhosted.org/packages/py3/t/tomli/tomli-1.2.2-py3-none-any.whl"
    list_url = "https://pypi.org/simple/tomli/"

    version('1.2.2', sha256='f04066f68f5554911363063a30b108d2b5a5b1a010aa8b6132af78489fe3aade', expand=False)
    version('1.2.1', sha256='8dd0e9524d6f386271a36b41dbf6c57d8e32fd96fd22b6584679dc569d20899f', expand=False)

    depends_on('python@3.6:', type=('build', 'run'))
