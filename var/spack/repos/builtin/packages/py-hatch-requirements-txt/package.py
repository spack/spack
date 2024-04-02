# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHatchRequirementsTxt(PythonPackage):
    """Hatchling plugin to read project dependencies from requirements.txt"""

    homepage = "https://github.com/repo-helper/hatch-requirements-txt"
    pypi = "hatch_requirements_txt/hatch_requirements_txt-0.4.0.tar.gz"

    license("MIT")

    version(
        "0.4.0",
        sha256="cb16fd5205d6d9c13641379ae75d63f538a29f05e377656f2f3d0e1931621d74",
        url="https://pypi.org/packages/5c/66/6fafc6e5ad4d4df49662b7696b39c512db13fb3566fc5ff0a394e8a2b133/hatch_requirements_txt-0.4.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-hatchling@0.21:")
        depends_on("py-packaging@21.3:")
