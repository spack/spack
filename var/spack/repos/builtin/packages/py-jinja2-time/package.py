# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJinja2Time(PythonPackage):
    """Jinja2 Extension for Dates and Times"""

    homepage = "https://github.com/hackebrot/jinja2-time"
    url = "https://github.com/hackebrot/jinja2-time/archive/0.2.0.tar.gz"

    license("MIT")

    version(
        "0.2.0",
        sha256="d3eab6605e3ec8b7a0863df09cc1d23714908fa61aa6986a845c20ba488b4efa",
        url="https://pypi.org/packages/6a/a1/d44fa38306ffa34a7e1af09632b158e13ec89670ce491f8a15af3ebcb4e4/jinja2_time-0.2.0-py2.py3-none-any.whl",
    )
