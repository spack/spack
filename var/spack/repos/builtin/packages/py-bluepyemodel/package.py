# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBluepyemodel(PythonPackage):
    """Python library to optimize and evaluate electrical models."""

    homepage = "https://github.com/BlueBrain/BluePyEModel"
    pypi = "bluepyemodel/bluepyemodel-0.0.57.tar.gz"

    version("0.0.57", sha256="0b91e39e5066ab4a996bd932577b49648169e549c5f05bb3f93e345b4b186093")

    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-ipyparallel@6.3:", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-gitpython", type=("build", "run"))
    depends_on("py-bluepyopt@1.12.12:", type=("build", "run"))
    depends_on("py-bluepyefe@2.2.0:", type=("build", "run"))
    depends_on("py-neurom@3.0:3", type=("build", "run"))
    depends_on("py-efel@3.1:", type=("build", "run"))
    depends_on("py-configparser", type=("build", "run"))
    depends_on("py-morph-tool@2.8:", type=("build", "run"))
    depends_on("py-fasteners@0.16:", type=("build", "run"))
    depends_on("neuron+python@8.0:", type=("build", "run"))
    depends_on("py-jinja2@3.0.3", when="@0.0.11:", type=("build", "run"))
    depends_on("py-currentscape@0.0.11:", type=("build", "run"))

    def patch(self):
        # This dependency has survived, even though the modules needing it were axed mid
        # 2021
        filter_file(r".*psycopg2-binary.*", "", "setup.py")
