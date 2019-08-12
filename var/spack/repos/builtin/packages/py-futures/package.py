# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFutures(PythonPackage):
    """Backport of the concurrent.futures package from Python 3.2"""

    homepage = "https://pypi.python.org/pypi/futures"
    url      = "https://pypi.io/packages/source/f/futures/futures-3.0.5.tar.gz"

    version('3.0.5', 'ced2c365e518242512d7a398b515ff95')

    depends_on('py-setuptools', type='build')
