# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPyeventsystem(PythonPackage):
    """An event driven middleware library for Python."""

    homepage = "https://github.com/cloudve/pyeventsystem"
    pypi = "pyeventsystem/pyeventsystem-0.1.0.tar.gz"

    license("MIT")

    version(
        "0.1.0",
        sha256="2a651eca3ec0b7e8600e2d4f042ab519b2d3bf74969e783b7a51fb87c506a7a6",
        url="https://pypi.org/packages/e5/d3/99dac9569f8e90c21889a6d91d187404eb831ceef4638c98c3ff8915ae44/pyeventsystem-0.1.0-py2.py3-none-any.whl",
    )
