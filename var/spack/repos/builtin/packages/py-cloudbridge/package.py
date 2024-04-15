# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCloudbridge(PythonPackage):
    """A simple layer of abstraction over multiple cloud providers."""

    homepage = "http://cloudbridge.cloudve.org"
    pypi = "cloudbridge/cloudbridge-3.1.0.tar.gz"

    license("MIT")

    version(
        "3.1.0",
        sha256="6b6c9464c25e5831339928e2043588c25b010d83b2c12508aeeb8cba048ee0c6",
        url="https://pypi.org/packages/cc/1e/2157f70d465f3bbfa34ed958bca581e6f33c945b511229e50b2a4f6339c2/cloudbridge-3.1.0-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-deprecation@2.0.7:", when="@2.1:")
        depends_on("py-pyeventsystem", when="@2:")
        depends_on("py-six@1.11:", when="@1.0.2:")
        depends_on("py-tenacity@6:", when="@2.1:")
