# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPytestWorkflow(PythonPackage):
    """A workflow-system agnostic testing framework
    that aims to make pipeline/workflow testing easy
    by using YAML files for the test configuration.
    """

    homepage = "https://github.com/LUMC/pytest-workflow"
    pypi = "pytest-workflow/pytest-workflow-1.6.0.tar.gz"

    license("AGPL-3.0-or-later")

    version(
        "1.6.0",
        sha256="bb1f1dbc2cfa4d4a9af45e7764fb8e65d8baa59cb0db72cf88ff0ad1590887e6",
        url="https://pypi.org/packages/09/3e/af45083f33ce8d4a412f9f7264254b689e6182c85619219fb8086294f158/pytest_workflow-1.6.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-jsonschema")
        depends_on("py-pytest@5.4:", when="@1.3:1")
        depends_on("py-pyyaml")
