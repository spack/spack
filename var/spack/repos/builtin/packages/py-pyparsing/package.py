# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyparsing(Package, PythonExtension):
    """Python parsing module."""

    homepage = "https://pyparsing-docs.readthedocs.io/en/latest/"
    # Must be installed from wheel to avoid circular dependency on build
    url = "https://files.pythonhosted.org/packages/py3/p/pyparsing/pyparsing-3.0.9-py3-none-any.whl"
    list_url = "https://pypi.org/simple/pyparsing/"

    import_modules = ["pyparsing"]

    version("3.0.9", sha256="5026bae9a10eeaefb61dab2f09052b9f4307d44aee4eda64b309723d8d206bbc", expand=False)
    version("3.0.6", sha256="04ff808a5b90911829c55c4e26f75fa5ca8a2f5f36aa3a51f68e27033341d3e4", expand=False)
    version("2.4.7", sha256="ef9d7589ef3c200abe66653d3f1ab1033c3c419ae9b9bdb1240a85b024efc88b", expand=False)
    version("2.4.2", sha256="d9338df12903bbf5d65a0e4e87c2161968b10d2e489652bb47001d82a9b028b4", expand=False)
    version("2.4.0", sha256="9b6323ef4ab914af344ba97510e966d64ba91055d6b9afa6b30799340e89cc03", expand=False)
    version("2.3.1", sha256="f6c5ef0d7480ad048c054c37632c67fca55299990fff127850181659eea33fc3", expand=False)

    extends("python")
    depends_on("py-installer", type="build")

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/{0}/p/pyparsing/pyparsing-{1}-{0}-none-any.whl"
        if version >= Version("3"):
            language = "py3"
        else:
            language = "py2.py3"
        return url.format(language, version)

    def install(self, spec, prefix):
        installer("--prefix", prefix, self.stage.archive_file)
