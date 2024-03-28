# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMsrestazure(PythonPackage):
    """AutoRest swagger generator Python client runtime.
    Azure-specific module."""

    homepage = "https://github.com/Azure/msrestazure-for-python"
    pypi = "msrestazure/msrestazure-0.6.3.tar.gz"

    version(
        "0.6.3",
        sha256="0ae7f903ff81631512beef39602c4104a8fe04cb7d166f28a1ec43c0f0985749",
        url="https://pypi.org/packages/01/70/4abd575d876428e3892ca6b7acafb59b53cb9923fa6aec2cbbf173495ce1/msrestazure-0.6.3-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-adal@0.6:", when="@0.5:")
        depends_on("py-msrest@0.6.0:", when="@0.6:")
