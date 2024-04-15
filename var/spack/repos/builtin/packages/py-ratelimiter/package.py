# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRatelimiter(PythonPackage):
    """Simple Python module providing rate limiting."""

    homepage = "https://github.com/RazerM/ratelimiter"
    pypi = "ratelimiter/ratelimiter-1.2.0.post0.tar.gz"

    maintainers("marcusboden")

    license("Apache-2.0")

    version(
        "1.2.0.post0",
        sha256="a52be07bc0bb0b3674b4b304550f10c769bbb00fead3072e035904474259809f",
        url="https://pypi.org/packages/51/80/2164fa1e863ad52cc8d870855fba0fbb51edd943edffd516d54b5f6f8ff8/ratelimiter-1.2.0.post0-py3-none-any.whl",
    )
