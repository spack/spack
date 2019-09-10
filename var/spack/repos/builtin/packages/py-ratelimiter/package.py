# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRatelimiter(PythonPackage):
    """Simple Python module providing rate limiting.
    """

    homepage = "https://github.com/RazerM/ratelimiter"
    url      = "https://pypi.io/packages/source/r/ratelimiter/ratelimiter-3.11.2.tar.gz"

    version('1.2.0', 'f724b256264afdeab0225ec174728b0f8af1afd1cc122463150daf226b411fb6')

    depends_on('py-setuptools', type=('build', 'run'))
