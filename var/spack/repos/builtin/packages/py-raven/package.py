# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRaven(PythonPackage):
    """Raven is a client for Sentry."""

    homepage = "https://github.com/getsentry/raven-python"
    pypi = "raven/raven-6.10.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "6.10.0",
        sha256="44a13f87670836e153951af9a3c80405d36b43097db869a36e92809673692ce4",
        url="https://pypi.org/packages/bd/8e/62e26a88c0a1bbae677200baf0767c1022321a6555634f8129e6d55c5ddc/raven-6.10.0-py2.py3-none-any.whl",
    )

    variant("flask", default=False, description="Build flask backend")

    with default_args(type=("build", "run")):
        depends_on("py-blinker@1.1:", when="@:6.2,6.4,6.6:+flask")
        depends_on("py-flask@0.8:", when="@:6.2,6.4,6.6:+flask")
