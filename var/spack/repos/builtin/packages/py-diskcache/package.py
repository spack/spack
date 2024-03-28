# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDiskcache(PythonPackage):
    """Disk Cache -- Disk and file backed persistent cache."""

    homepage = "http://www.grantjenks.com/docs/diskcache/"
    pypi = "diskcache/diskcache-4.1.0.tar.gz"

    license("Apache-2.0")

    version(
        "5.2.1",
        sha256="6e8137c778fd2752b93c8a8f944e939b3665d645b46774d8537dd3528ac3baa1",
        url="https://pypi.org/packages/6a/5e/3deb8f9c83bead2af6f2cda97c4400516488464fede2853875a81e502953/diskcache-5.2.1-py3-none-any.whl",
    )
    version(
        "4.1.0",
        sha256="69b253a6ffe95bb4bafb483b97c24fca3c2c6c47b82e92b36486969a7e80d47d",
        url="https://pypi.org/packages/ee/cc/d992e1d886d5ce15d2622c2e89b6de52b48312c6f05e34b7ee881b4ccb02/diskcache-4.1.0-py2.py3-none-any.whl",
    )
