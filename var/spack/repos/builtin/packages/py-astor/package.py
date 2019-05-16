# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAstor(PythonPackage):
    """Astor is designed to allow easy manipulation of Python source via the AST."""

    homepage = "https://pypi.python.org/pypi/astor"
    url      = "https://cosmo-pypi.phys.ethz.ch/simple/astor/0.6/astor-0.6.tar.gz"

    version('0.6', '3ab0066af00173e117c4c20b53c463ea')

    depends_on('py-setuptools', type='build')
