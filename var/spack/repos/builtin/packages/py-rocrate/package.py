# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRocrate(PythonPackage):
    """RO-Crate metadata generator/parser"""

    homepage = "https://github.com/ResearchObject/ro-crate-py/"
    pypi = "rocrate/rocrate-0.7.0.tar.gz"

    license("Apache-2.0")

    version(
        "0.7.0",
        sha256="86443b621e4eb31eb501c202402ce0d8d8b0e9d5f8a446296d8df83ac21c0d53",
        url="https://pypi.org/packages/3b/b9/20dea9f6f79c4032fc2ab971bacfcd91a59e452d66cd3d04e6a1a3ef7a0f/rocrate-0.7.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.6.1:")
        depends_on("py-arcp@0.2.1:")
        depends_on("py-click", when="@0.4:")
        depends_on("py-galaxy2cwl")
        depends_on("py-jinja2")
        depends_on("py-python-dateutil")
        depends_on("py-requests", when="@0.3.1:")
