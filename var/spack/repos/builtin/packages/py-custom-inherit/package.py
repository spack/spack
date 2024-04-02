# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCustomInherit(PythonPackage):
    """A Python package that provides customized docstring inheritance schemes
    between derived classes and their parents.
    """

    homepage = "https://github.com/rsokl/custom_inherit"
    pypi = "custom_inherit/custom_inherit-2.2.2.tar.gz"

    maintainers("snehring")

    license("MIT")

    version(
        "2.4.1",
        sha256="313f9594d98e79a7fbf58d9ad368fd29adc97572d886975dbd8c7032b14abc6a",
        url="https://pypi.org/packages/c0/0c/f0967273bd2213adaafbd8754fa36f03ba21273ce03f70a83551fe12b0f1/custom_inherit-2.4.1-py3-none-any.whl",
    )
    version(
        "2.2.2",
        sha256="8ffbf5750e470185fd320b3778ffcd2e67f69c641d6092c5aa638da04138767b",
        url="https://pypi.org/packages/0d/79/5b24b10d4c80fd9ba76a90e8e7f2611b18941337d82576576f020bd3a4bf/custom_inherit-2.2.2-py3-none-any.whl",
    )
