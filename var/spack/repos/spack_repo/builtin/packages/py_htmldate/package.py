# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyHtmldate(PythonPackage):
    """Fast and robust date extraction from web pages, with Python or on the command-line."""

    homepage = "https://htmldate.readthedocs.io/en/latest/"
    pypi = "htmldate/htmldate-1.9.3.tar.gz"

    license("Apache-2.0")

    version("1.9.3", sha256="ac0caf4628c3ded4042011e2d60dc68dfb314c77b106587dd307a80d77e708e9")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-charset-normalizer@3.4.0:", type=("build", "run"))
    depends_on("py-dateparser@1.1.2:", type=("build", "run"))
    depends_on("py-lxml@4.9.2", when="platform=darwin ^python@:3.8", type=("build", "run"))
    depends_on("py-lxml@5.3.0:5", when="platform=linux", type=("build", "run"))
    depends_on("py-lxml@5.3.0:5", when="^python@3.9:", type=("build", "run"))
    depends_on("py-python-dateutil@2.9.0.post0:", type=("build", "run"))
    depends_on("py-urllib3@1.26:2", type=("build", "run"))
