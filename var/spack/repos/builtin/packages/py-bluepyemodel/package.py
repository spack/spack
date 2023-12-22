# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBluepyemodel(PythonPackage):
    """Python library to optimize and evaluate electrical models."""

    homepage = "https://github.com/BlueBrain/BluePyEModel"
    pypi = "bluepyemodel/bluepyemodel-0.0.46.tar.gz"

    version("0.0.46", sha256="ad4c125e491f3337fcc341a4f389b8a616d883ce50fd77d9fb0ea6e13be5da61")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")

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
