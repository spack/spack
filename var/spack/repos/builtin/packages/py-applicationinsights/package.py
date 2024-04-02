# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyApplicationinsights(PythonPackage):
    """This project extends the Application Insights API surface to support
    Python."""

    homepage = "https://github.com/Microsoft/ApplicationInsights-Python"
    pypi = "applicationinsights/applicationinsights-0.11.9.tar.gz"

    # 'applicationinsights.django' requires 'django', but 'django' isn't listed as a
    # dependency. Leave out of 'import_modules' list to avoid unnecessary dependency.
    import_modules = [
        "applicationinsights",
        "applicationinsights.flask",
        "applicationinsights.exceptions",
        "applicationinsights.requests",
        "applicationinsights.channel",
        "applicationinsights.channel.contracts",
        "applicationinsights.logging",
    ]

    license("MIT")

    version(
        "0.11.9",
        sha256="b88bc5a41385d8e516489128d5e63f8c52efe597a3579b1718d1ab2f7cf150a2",
        url="https://pypi.org/packages/a1/53/234c53004f71f0717d8acd37876e0b65c121181167057b9ce1b1795f96a0/applicationinsights-0.11.9-py2.py3-none-any.whl",
    )
