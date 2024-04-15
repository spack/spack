# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCallmonitor(PythonPackage):
    """A Simple Tool to Monitor and Log Function Calls"""

    homepage = "https://github.com/JBlaschke/call-monitor"
    pypi = "callmonitor/callmonitor-0.3.7.tar.gz"

    maintainers("DaxLynch")

    version(
        "0.3.7",
        sha256="352c0f3bd8268b38a8f5e7e4dd80d4bdbafac7e6520860234b1f91de95888277",
        url="https://pypi.org/packages/9f/31/8035151093faa5b2fe6d3bea7136643fe718689334825396f371f947a095/callmonitor-0.3.7-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-numpy", when="@0.3:")
