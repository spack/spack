# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFreezegun(PythonPackage):
    """FreezeGun is a library that allows your Python tests to travel
    through time by mocking the datetime module."""

    homepage = "https://github.com/spulec/freezegun"
    pypi = "freezegun/freezegun-0.3.12.tar.gz"

    license("Apache-2.0")

    version(
        "0.3.12",
        sha256="edfdf5bc6040969e6ed2e36eafe277963bdc8b7c01daeda96c5c8594576c9390",
        url="https://pypi.org/packages/81/98/801900ea24536928a99e40a815812c1bc7d7f833d53ec53f216d8330db7d/freezegun-0.3.12-py2.py3-none-any.whl",
    )
