# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyNeuror(PythonPackage):
    """A collection of tools to repair morphologies."""

    homepage = "https://github.com/BlueBrain/NeuroR"
    git = "https://github.com/BlueBrain/NeuroR.git"
    pypi = "neuror/NeuroR-1.2.3.tar.gz"

    version("develop", branch="master")
    version("1.6.4", sha256="a65c0e1814c38326a344f03c1f5f92ab4db721c5541888b2acb9ffc5a7adac50")

    depends_on("py-setuptools", type=("build", "run"))

    depends_on("py-click@6.7:", type=("build", "run"))
    depends_on("py-jsonschema", type=("build", "run"))
    depends_on("py-matplotlib@2.2.3:", type=("build", "run"))
    depends_on("py-morph-tool@2.9.0:2.999", type=("build", "run"))
    depends_on("py-morphio@3.0.0:3.999", type=("build", "run"))
    depends_on("py-neurom@3.0.1:3.999", type=("build", "run"))
    depends_on("py-numpy@1.19.2:", type=("build", "run"))
    depends_on("py-nptyping@2:", type=("build", "run"))
    depends_on("py-pandas@0.24.2:", type=("build", "run"))
    depends_on("py-pyquaternion@0.9.2:", type=("build", "run"))
    depends_on("py-scipy@1.2.0:", type=("build", "run"))
