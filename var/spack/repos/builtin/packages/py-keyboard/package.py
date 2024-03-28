# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKeyboard(PythonPackage):
    """Take full control of your keyboard with this small
    Python library. Hook global events, register hotkeys,
    simulate key presses and much more."""

    homepage = "https://github.com/boppreh/keyboard"
    pypi = "keyboard/keyboard-0.13.5.zip"

    license("MIT")

    version(
        "0.13.5",
        sha256="8e9c2422f1217e0bd84489b9ecd361027cc78415828f4fe4f88dd4acd587947b",
        url="https://pypi.org/packages/55/88/287159903c5b3fc6d47b651c7ab65a54dcf9c9916de546188a7f62870d6d/keyboard-0.13.5-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-pyobjc", when="@0.13.2: platform=darwin")
        depends_on("py-pyobjc", when="@0.13:0.13.0")

    # depends_on('py-pyobjc', when='platform=darwin', type=('build', 'run'))

    # Until py-pyobjc can be created, specifying conflict with platform=darwin
    conflicts("platform=darwin")
