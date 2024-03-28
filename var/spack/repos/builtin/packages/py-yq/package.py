# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyYq(PythonPackage):
    """yq takes YAML input, converts it to JSON, and pipes it to jq"""

    homepage = "https://github.com/kislyuk/yq"
    pypi = "yq/yq-2.12.2.tar.gz"

    maintainers("qwertos")

    license("Apache-2.0")

    version(
        "2.12.2",
        sha256="9fdf4487a6dbf985ca1d357ec93f926d982813e8e896e8892bae95162b6defe3",
        url="https://pypi.org/packages/97/0a/b5a11f52ac794fbf800e05b6268283e6aea412a3faa5ae95e67eb29ea5e0/yq-2.12.2-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-argcomplete@1.8.1:", when="@2.10:")
        depends_on("py-pyyaml@3.11:", when="@2.8:2.12")
        depends_on("py-setuptools", when="@2.8:2.12")
        depends_on("py-toml@0.10:", when="@2.12:3.1")
        depends_on("py-xmltodict@0.11:", when="@2.8:")
