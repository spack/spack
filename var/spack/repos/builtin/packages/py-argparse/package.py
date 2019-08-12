# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyArgparse(PythonPackage):
    """Python command-line parsing library."""

    homepage = "https://github.com/ThomasWaldmann/argparse/"
    url      = "https://pypi.io/packages/source/a/argparse/argparse-1.4.0.tar.gz"

    version('1.4.0', '08062d2ceb6596fcbc5a7e725b53746f')

    depends_on('python@2.3:')

    depends_on('py-setuptools', type='build')
