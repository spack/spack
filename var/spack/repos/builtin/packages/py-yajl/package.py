# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from shutil import rmtree
from os import symlink


class PyYajl(PythonPackage):
    """Python bindings for the Yajl JSON encoder/decoder library."""

    homepage = "https://github.com/rtyler/py-yajl"
    url      = "https://files.pythonhosted.org/packages/70/5a/57ed8b430a55e2bfc9c4ea0a263f41f4d2fe5d962ff073c8af117da78be1/yajl-0.3.5.tar.gz"

    version('0.3.5', sha256='432321ea613692a4782a2368a300f57b59c64a3c8508c7465af3fdc045e7bcc2')

    depends_on('py-setuptools', type='build')
