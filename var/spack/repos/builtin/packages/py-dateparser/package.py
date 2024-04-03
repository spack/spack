# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDateparser(PythonPackage):
    """dateparser -- python parser for human readable dates"""

    homepage = "https://github.com/scrapinghub/dateparser"
    pypi = "dateparser/dateparser-0.7.2.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.7.2",
        sha256="983d84b5e3861cb0aa240cad07f12899bb10b62328aae188b9007e04ce37d665",
        url="https://pypi.org/packages/82/9d/51126ac615bbc4418478d725a5fa1a0f112059f6f111e4b48cfbe17ef9d0/dateparser-0.7.2-py2.py3-none-any.whl",
    )

    variant("calendars", default=True, description="Add calendar libraries")

    with default_args(type="run"):
        depends_on("py-python-dateutil", when="@0.3.5:")
        depends_on("py-pytz")
        depends_on("py-regex", when="@0.3.3:0.7.2")
        depends_on("py-tzlocal", when="@0.5:")
