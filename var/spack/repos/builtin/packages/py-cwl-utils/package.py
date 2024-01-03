# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCwlUtils(PythonPackage):
    """Python Utilities and Autogenerated Classes
    for loading and parsing CWL v1.0, CWL v1.1, and CWL v1.2 documents.
    """

    homepage = "https://github.com/common-workflow-language/cwl-utils"
    pypi = "cwl-utils/cwl-utils-0.21.tar.gz"

    license("Apache-2.0")

    version("0.21", sha256="583f05010f7572f3a69310325472ccb6efc2db7f43dc6428d03552e0ffcbaaf9")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-cwl-upgrader@1.2.3:", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-rdflib", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-cachecontrol", type=("build", "run"))
    depends_on("py-schema-salad@8.3.20220825114525:8", type=("build", "run"))
