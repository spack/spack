# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAppnope(PythonPackage):
    """Disable App Nap on OS X 10.9"""

    homepage = "https://github.com/minrk/appnope"
    url      = "https://pypi.io/packages/source/a/appnope/appnope-0.1.0.tar.gz"

    version('0.1.0', '932fbaa73792c9b06754755a774dcac5')
