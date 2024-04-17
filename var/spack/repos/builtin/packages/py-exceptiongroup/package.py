# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyExceptiongroup(PythonPackage):
    """A backport of the BaseExceptionGroup and ExceptionGroup classes from Python 3.11."""

    homepage = "https://github.com/agronholm/exceptiongroup"
    pypi = "exceptiongroup/exceptiongroup-1.0.4.tar.gz"

    version(
        "1.1.1",
        sha256="232c37c63e4f682982c8b6459f33a8981039e5fb8756b2074364e5055c498c9e",
        url="https://pypi.org/packages/61/97/17ed81b7a8d24d8f69b62c0db37abbd8c0042d4b3fc429c73dab986e7483/exceptiongroup-1.1.1-py3-none-any.whl",
    )
    version(
        "1.0.4",
        sha256="542adf9dea4055530d6e1279602fa5cb11dab2395fa650b8674eaec35fc4a828",
        url="https://pypi.org/packages/ce/2e/9a327cc0d2d674ee2d570ee30119755af772094edba86d721dda94404d1a/exceptiongroup-1.0.4-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:")
