# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRequestsCache(PythonPackage):
    """A persistent HTTP cache that provides an easy way
    to get better performance with the python requests library.
    """

    homepage = "https://github.com/requests-cache/requests-cache"
    pypi = "requests-cache/requests_cache-0.9.7.tar.gz"

    license("BSD-2-Clause")

    version(
        "0.9.7",
        sha256="3f57badcd8406ecda7f8eaa8145afd0b180c5ae4ff05165a2c4d40f3dc88a6e5",
        url="https://pypi.org/packages/65/a8/404ed794200edecf53f952066a8d33887924c6956ef0db71fccb90f1f68f/requests_cache-0.9.7-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:3", when="@:1.1")
        depends_on("py-appdirs@1.4.4:", when="@0.9.6:0.9")
        depends_on("py-attrs@21.2:", when="@0.9.6:0.9,0.10.0.dev1:")
        depends_on("py-cattrs@22.2:", when="@0.9.7:0.9,1.0.0-beta1:")
        depends_on("py-requests@2.22:", when="@0.9.6:0.9,1.0.0-alpha2:")
        depends_on("py-url-normalize@1.4:", when="@0.9.6:0.9,1.0.0-alpha2:")
        depends_on("py-urllib3@1.25.5:", when="@0.9.6:0.9,0.10.0.dev1:")

    # depends_on("py-platformdirs@2.5:", type=("build", "run"))  # will be in future versions
