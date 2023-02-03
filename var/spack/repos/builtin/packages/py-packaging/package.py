# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPackaging(Package, PythonExtension):
    """Core utilities for Python packages."""

    homepage = "https://github.com/pypa/packaging"
    # Must be installed from wheel to avoid circular dependency on build
    url = "https://files.pythonhosted.org/packages/py3/p/packaging/packaging-23.0-py3-none-any.whl"
    list_url = "https://pypi.org/simple/packaging/"

    version("23.0", sha256="714ac14496c3e68c99c29b00845f7a2b85f3bb6f1078fd9f72fd20f0570002b2", expand=False)
    version("21.3", sha256="ef103e05f519cdc783ae24ea4e2e0f508a9c99b2d4969652eed6a2e1ea5bd522", expand=False)
    version("21.0", sha256="c86254f9220d55e31cc94d69bade760f0847da8000def4dfe1c6b872fd14ff14", expand=False)
    version("20.9", sha256="67714da7f7bc052e064859c05c595155bd1ee9f69f76557e21f051443c20947a", expand=False)
    version("19.2", sha256="d9551545c6d761f3def1677baf08ab2a3ca17c56879e70fecba2fc4dde4ed108", expand=False)
    version("19.1", sha256="a7ac867b97fdc07ee80a8058fe4435ccd274ecc3b0ed61d852d7d53055528cf9", expand=False)
    version("19.0", sha256="9e1cbf8c12b1f1ce0bb5344b8d7ecf66a6f8a6e91bcb0c84593ed6d3ab5c4ab3", expand=False)
    version("17.1", sha256="e9215d2d2535d3ae866c3d6efc77d5b24a0192cce0ff20e42896cc0664f889c0", expand=False)
    version("16.8", sha256="99276dc6e3a7851f32027a68f1095cd3f77c148091b092ea867a351811cfe388", expand=False)

    extends("python")
    depends_on("py-installer", type="build")

    depends_on("py-pyparsing@2.0.2:3.0.4,3.0.6:", when="@21.3:21", type=("build", "run"))
    depends_on("py-pyparsing@2.0.2:2", when="@21.1:21.2", type=("build", "run"))
    depends_on("py-pyparsing@2.0.2:", when="@:21.0", type=("build", "run"))
    depends_on("py-six", when="@:20.7", type=("build", "run"))
    depends_on("py-attrs", when="@19.1", type=("build", "run"))

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/{0}/p/packaging/packaging-{1}-{0}-none-any.whl"
        if version >= Version("21"):
            language = "py3"
        else:
            language = "py2.py3"
        return url.format(language, version)

    def install(self, spec, prefix):
        installer("--prefix", prefix, self.stage.archive_file)
