# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyPydap(PythonPackage):
    """An implementation of the Data Access Protocol."""

    homepage = "https://www.pydap.org/en/latest/"
    pypi = "pydap/pydap-3.5.5.tar.gz"
    license("MIT")

    version("3.5.5", sha256="0f8ca9b4e244c4d345d0b5269c4ebc886fcd0778b828e5ae1415b7ea5341eabd")
    version("3.2.2", sha256="86326642e24f421595a74b0f9986da76d7932b277768f501fe214d72592bdc40")

    depends_on("python@3.10:", type=("build", "run"), when="@3.5:")

    depends_on("py-setuptools@64:", type="build", when="@3.5:")
    depends_on("py-setuptools-scm@8: +toml", type="build", when="@3.5:")
    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-webob", type=("build", "run"))
    depends_on("py-beautifulsoup4", type=("build", "run"))

    depends_on("py-requests", type="build", when="@3.5:")
    depends_on("py-requests-cache", type="build", when="@3.5:")
    depends_on("py-scipy", type="build", when="@3.5:")
    depends_on("py-lxml", type="build", when="@3.5:")

    depends_on("py-jinja2", type=("build", "run"), when="@:3.4")
    depends_on("py-docopt", type=("build", "run"), when="@:3.4")
    depends_on("py-six@1.4.0:", type=("build", "run"), when="@:3.4")

    def url_for_version(self, version):
        if version < Version("3.5"):
            return f"https://files.pythonhosted.org/packages/source/P/Pydap/Pydap-{version}.tar.gz"

        return super().url_for_version(version)
