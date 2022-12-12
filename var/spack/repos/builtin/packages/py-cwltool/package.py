# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCwltool(PythonPackage):
    """Common workflow language reference implementation"""

    homepage = "https://github.com/common-workflow-language/cwltool"
    pypi = "cwltool/cwltool-3.1.20221201130942.tar.gz"

    version(
        "3.1.20221201130942",
        sha256="0152d8cdf6acaf3620f557b442941f577bff2851d9e2e866e6051ea48a37bdbe",
    )
    version(
        "3.1.20221109155812",
        sha256="82676ea315ce84fc4057d92c040af15dde3e897527ea4ae70c1033b0eca20c2a",
    )

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-requests@2.4.3:", type=("build", "run"))
    depends_on("py-ruamel.yaml@0.16.0:0.17.21", when="^python@3.10:", type=("build", "run"))
    depends_on("py-ruamel.yaml@0.15:0.17.21", type=("build", "run"))
    depends_on("py-rdflib@4.2.2:6.2.999999", type=("build", "run"))
    depends_on("py-rdflib@4.2.2:5.999999", when="^python@:3.6", type=("build", "run"))
    depends_on("py-shellescape@3.4.1:3.8.999999", type=("build", "run"))
    depends_on("py-schema-salad@8.2.20211104054942:8.999999", type=("build", "run"))
    depends_on("py-prov@1.5.1", type=("build", "run"))
    depends_on("py-bagit@1.8.1", type=("build", "run"))
    depends_on("py-mypy-extensions", type=("build", "run"))
    depends_on("py-psutil@5.6.6:", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))
    depends_on("py-coloredlogs", type=("build", "run"))
    depends_on("py-pydot@1.4.1:", type=("build", "run"))
    depends_on("py-argcomplete@1.12.0:", type=("build", "run"))
    depends_on("py-pyparsing@:3.0.1,3.0.3:", type=("build", "run"))
    depends_on("py-pyparsing@:3", when="^python@:3.6", type=("build", "run"))
    depends_on("py-cwl-utils@0.19:", type=("build", "run"))
