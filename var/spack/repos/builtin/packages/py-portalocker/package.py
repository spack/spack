# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPortalocker(PythonPackage):
    """Portalocker is a library to provide an easy API to file locking."""

    homepage = "https://github.com/WoLpH/portalocker"
    pypi = "portalocker/portalocker-2.5.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "2.5.1",
        sha256="400bae275366e7b840d4baad0654c6ec5994e07c40c423d78e9e1340279b8352",
        url="https://pypi.org/packages/a9/0a/21422dc681e3e59ce5ec4051015de4c2074bd0e6759099c018471f3dc4e3/portalocker-2.5.1-py2.py3-none-any.whl",
    )
    version(
        "1.6.0",
        sha256="094bd1e4b2bccdfcb586fe4ccf0f3229cb08f6ec66418bef541c69103265c3ed",
        url="https://pypi.org/packages/64/03/9abfb3374d67838daf24f1a388528714bec1debb1d13749f0abd7fb07cfb/portalocker-1.6.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-pywin32@226:", when="@2.4: platform=windows")
