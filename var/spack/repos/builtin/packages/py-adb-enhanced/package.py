# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAdbEnhanced(PythonPackage):
    """ADB-Enhanced is a Swiss-army knife for Android testing and
    development. A command-line interface to trigger various scenarios
    like screen rotation, battery saver mode, data saver mode, doze
    mode, permission grant/revocation."""

    homepage = "https://opencollective.com/ashishb"
    url = "https://github.com/ashishb/adb-enhanced/archive/2.5.4.tar.gz"

    license("Apache-2.0")

    version(
        "2.5.10",
        sha256="19e9462702d1d20ee023686e128a43d15149411c7cd2838639df7d6df6d282ee",
        url="https://pypi.org/packages/2b/ae/0515f15799a811d7e06c60ae4bcc7ac3df8f6c5024a8fb6093e0a0cc6d77/adb_enhanced-2.5.10-py3-none-any.whl",
    )
    version(
        "2.5.4",
        sha256="f8c4a1c4ee7ca82210b6f2472763c0239cd63c9c58c5b4b2b7d0edf3c7c5180e",
        url="https://pypi.org/packages/fb/48/c9325bd726bebddf68f77da0d1ac90b6542c97121d008423f5d68f77e1ac/adb_enhanced-2.5.4-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-asyncio", when="@2.2:2.5.4")
        depends_on("py-docopt")
        depends_on("py-future", when="@:2.5.4")
        depends_on("py-psutil")
