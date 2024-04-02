# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFolium(PythonPackage):
    """Make beautiful maps with Leaflet.js & Python."""

    homepage = "https://python-visualization.github.io/folium"
    pypi = "folium/folium-0.16.0.tar.gz"

    license("MIT")

    version(
        "0.16.0",
        sha256="ba72505db18bef995c880da19457d2b10c931db8059af5f6ccec9310d262b584",
        url="https://pypi.org/packages/b9/98/9ba4b9d2d07dd32765ddb4e4c189dcbdd7dca4d5a735e2e4ea756f40c36b/folium-0.16.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.15:")
        depends_on("py-branca@0.6:", when="@0.14:")
        depends_on("py-jinja2@2.9:")
        depends_on("py-numpy")
        depends_on("py-requests")
        depends_on("py-xyzservices", when="@0.15.1:")
