# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCwlUpgrader(PythonPackage):
    """Common Workflow Language standalone document upgrader"""

    homepage = "https://github.com/common-workflow-language/cwl-upgrader"
    pypi = "cwl-upgrader/cwl-upgrader-1.2.4.tar.gz"

    license("Apache-2.0")

    version(
        "1.2.4",
        sha256="7d2b8b835f9f4c1068dfead0b7d9f60a88f27e5368d54d0301f2135942b35619",
        url="https://pypi.org/packages/4f/b4/11831dd7fb8abb19980dff3bad55bc7d11dc9d9d9f8e2583adc4ca91d2ea/cwl_upgrader-1.2.4-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3", when="@1:1.2.8")
        depends_on("py-ruamel-yaml@0.15.98:0.17.21", when="@1.2.3:1.2.5 ^python@3.9:")
        depends_on("py-ruamel-yaml@0.16:0.17.21", when="@1.2.3:1.2.5 ^python@3.10:")
        depends_on("py-ruamel-yaml@0.15.78:0.17.21", when="@1.2.3:1.2.5 ^python@3.8:")
        depends_on("py-ruamel-yaml@0.15.71:0.17.21", when="@1.2.3:1.2.4")
        depends_on("py-schema-salad", when="@1.1:")
        depends_on("py-setuptools", when="@0.4:")
