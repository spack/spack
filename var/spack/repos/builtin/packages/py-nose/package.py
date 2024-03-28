# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNose(PythonPackage):
    """nose extends the test loading and running features of unittest,
    making it easier to write, find and run tests."""

    pypi = "nose/nose-1.3.4.tar.gz"

    license("LGPL-2.1-or-later")

    version(
        "1.3.7",
        sha256="9ff7c6cc443f8c51994b34a667bbcf45afd6d945be7477b52e97516fd17c53ac",
        url="https://pypi.org/packages/15/d8/dd071918c040f50fa1cf80da16423af51ff8ce4a0f2399b7bf8de45ac3d9/nose-1.3.7-py3-none-any.whl",
    )
    version(
        "1.3.6",
        sha256="e19b4f8a495681c367ab56c3c04f8bef30ddd7907ddfd9bee663a3f3286762b6",
        url="https://pypi.org/packages/91/dc/1211a07f7c3a4e3b02a7e6e2c726fb763d13357d712987151a4ca44f821a/nose-1.3.6-py3-none-any.whl",
    )
    version(
        "1.3.4",
        sha256="cc8aebdec5a5fb989912f157f77b3c21a5e2f2da623af90a7b476b106a834abf",
        url="https://pypi.org/packages/07/c6/0667b318b01832320829b32b9858bc8897710b373d3f7c88a0e6fca742e9/nose-1.3.4-py3-none-any.whl",
    )
