# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBluepyemodel(PythonPackage):
    """Python library to optimize and evaluate electrical models."""

    homepage = "https://bbpgitlab.epfl.ch/cells/bluepyemodel"
    git = "ssh://git@bbpgitlab.epfl.ch/cells/bluepyemodel.git"

    version("0.0.11", tag="bluepyemodel-v0.0.11")
    version("0.0.8", tag="BluePyEModel-v0.0.8")

    depends_on("py-setuptools", type="build")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-ipyparallel@6.3:", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-gitpython", type=("build", "run"))
    depends_on("py-bluepyopt@1.12.12:", type=("build", "run"))
    depends_on("py-bluepyefe", type=("build", "run"))
    depends_on("py-neurom@3.0:3", type=("build", "run"))
    depends_on("py-efel@3.1:", type=("build", "run"))
    depends_on("py-configparser", type=("build", "run"))
    depends_on("py-bluepy@2.4:", when="@0.0.8", type=("build", "run"))
    depends_on("py-morph-tool@2.8:", type=("build", "run"))
    depends_on("py-fasteners@0.16:", type=("build", "run"))
    depends_on("neuron+python@8.0:", type=("build", "run"))
    depends_on("py-jinja2@3.0.3", when="@0.0.11:", type=("build", "run"))
    # missing but needed
    depends_on("py-click@7.0:", when="@0.0.8", type=("build", "run"))
    depends_on("py-matplotlib@2.2:", type=("build", "run"))
    # extra
    depends_on("py-bluepyparallel@0.0.3:", when="@0.0.8", type=("build", "run"))
    depends_on("py-bglibpy@4.4:", type=("build", "run"))
    depends_on("py-seaborn@0.11:", when="@0.0.8", type=("build", "run"))

    def patch(self):
        # This dependency has survived, even though the modules needing it were axed mid
        # 2021
        filter_file(r".*psycopg2-binary.*", "", "setup.py")
