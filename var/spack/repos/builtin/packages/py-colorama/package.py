# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyColorama(PythonPackage):
    """Cross-platform colored terminal text."""

    homepage = "https://github.com/tartley/colorama"
    url      = "https://pypi.io/packages/source/c/colorama/colorama-0.3.7.tar.gz"

    version('0.3.7', sha256='e043c8d32527607223652021ff648fbb394d5e19cba9f1a698670b338c9d782b')

    depends_on('py-setuptools', type='build')
