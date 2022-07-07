# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyxdg(PythonPackage):
    """Python library to access freedesktop.org standards."""

    pypi = "pyxdg/pyxdg-0.28.tar.gz"

    version('0.28', sha256='3267bb3074e934df202af2ee0868575484108581e6f3cb006af1da35395e88b4')

    extends('python', ignore=r'bin/pytest')
    depends_on('py-setuptools', type='build')
