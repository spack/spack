# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPromptToolkit(PythonPackage):
    """Library for building powerful interactive command lines in Python"""

    homepage = "https://pypi.python.org/pypi/prompt_toolkit"
    url      = "https://pypi.io/packages/source/p/prompt_toolkit/prompt_toolkit-1.0.9.tar.gz"

    version('1.0.9', 'a39f91a54308fb7446b1a421c11f227c')

    depends_on('py-setuptools', type='build')
    depends_on('py-six@1.9.0:', type=('build', 'run'))
    depends_on('py-wcwidth', type=('build', 'run'))
