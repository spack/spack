# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyConvertdate(PythonPackage):
    """Converts between Gregorian dates and other calendar
    systems.Calendars included: Baha'i, French Republican, Hebrew,
    Indian Civil, Islamic, ISO, Julian, Mayan and Persian."""

    homepage = "https://github.com/fitnr/convertdate/"
    pypi = "convertdate/convertdate-2.2.0.tar.gz"

    license("MIT")

    version(
        "2.2.0",
        sha256="fc34133ef6ceb31738cf1169b528ba487d0164d69f4451a7cef206887c45b71d",
        url="https://pypi.org/packages/c9/f8/02a18000b0fbfd714f78aa16359796727a181e80f679682e3f62771a5c23/convertdate-2.2.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-pymeeus@0.3.6:", when="@2.2:2.3.0")
        depends_on("py-pytz@2014.10:2019", when="@2.1.3:2.2.0")
