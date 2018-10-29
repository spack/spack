# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyColorama(PythonPackage):
    """Cross-platform colored terminal text."""

    homepage = "https://github.com/tartley/colorama"
    url      = "https://pypi.io/packages/source/c/colorama/colorama-0.3.7.tar.gz"

    version('0.3.7', '349d2b02618d3d39e5c6aede36fe3c1a')

    depends_on('py-setuptools', type='build')
