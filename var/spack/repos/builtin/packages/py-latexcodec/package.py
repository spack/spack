# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLatexcodec(PythonPackage):
    """A lexer and codec to work with LaTeX code in Python."""

    homepage = "http://latexcodec.readthedocs.io"
    url      = "https://pypi.io/packages/source/l/latexcodec/latexcodec-1.0.4.tar.gz"

    import_modules = ['latexcodec']

    version('1.0.4', '72010ec2a55227a5802239cff6fd32d6')

    depends_on('py-setuptools', type='build')
    depends_on('py-six@1.4.1:', type=('build', 'run'))
