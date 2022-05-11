# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PyImportlib(PythonPackage):
    """Packaging for importlib from Python 2.7"""

    homepage = "https://github.com/brettcannon/importlib"
    pypi = "importlib/importlib-1.0.4.zip"

    version('1.0.4', sha256='b6ee7066fea66e35f8d0acee24d98006de1a0a8a94a8ce6efe73a9a23c8d9826')

    # pip silently replaces distutils with setuptools
    depends_on('py-setuptools', type='build')
