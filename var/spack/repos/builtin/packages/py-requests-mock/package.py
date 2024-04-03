# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRequestsMock(PythonPackage):
    """Mock out responses from the requests package."""

    homepage = "https://requests-mock.readthedocs.io/"
    pypi = "requests-mock/requests-mock-1.7.0.tar.gz"

    version(
        "1.7.0",
        sha256="510df890afe08d36eca5bb16b4aa6308a6f85e3159ad3013bac8b9de7bd5a010",
        url="https://pypi.org/packages/8c/f1/66c54a412543b29454102ae74b1454fce2d307b1c36e6bd2e9818394df88/requests_mock-1.7.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-requests@2.3:", when="@1.7:1.11")
        depends_on("py-six", when="@:1.11")
