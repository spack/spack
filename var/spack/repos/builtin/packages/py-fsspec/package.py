# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFsspec(PythonPackage):
    """A specification for pythonic filesystems."""

    homepage = "https://github.com/intake/filesystem_spec"
    url      = "https://pypi.io/packages/source/f/fsspec/fsspec-0.4.4.tar.gz"

    version('0.4.4', sha256='97697a46e8bf8be34461c2520d6fc4bfca0ed749b22bb2b7c21939fd450a7d63')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
