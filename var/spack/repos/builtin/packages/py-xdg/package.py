# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXdg(PythonPackage):
    """Python library to access freedesktop.org standards."""

    pypi = "xdg/xdg-5.1.1.tar.gz"

    version('5.1.1', sha256='aa619f26ccec6088b2a6018721d4ee86e602099b24644a90a8d3308a25acd06c')

    extends('python', ignore=r'bin/pytest')
    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-poetry-core@1.0.0:', type='build')
    depends_on('py-setuptools', type='build')
