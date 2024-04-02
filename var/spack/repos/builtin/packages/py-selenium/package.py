# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySelenium(PythonPackage):
    """Python language bindings for Selenium WebDriver.

    The selenium package is used to automate web browser interaction from
    Python."""

    homepage = "https://github.com/SeleniumHQ/selenium/"
    pypi = "selenium/selenium-3.141.0.tar.gz"

    license("Apache-2.0")

    version(
        "3.141.0",
        sha256="2d7131d7bc5a5b99a2d9b04aaf2612c411b03b8ca1b1ee8d3de5845a9be2cb3c",
        url="https://pypi.org/packages/80/d6/4294f0b4bce4de0abf13e17190289f9d0613b0a44e5dd6a7f5ca98459853/selenium-3.141.0-py2.py3-none-any.whl",
    )
