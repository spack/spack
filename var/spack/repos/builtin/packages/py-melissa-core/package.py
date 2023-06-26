# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMelissaCore(PythonPackage):
    """Melissa is a file-avoiding, adaptive, fault-tolerant and elastic
    framework, to run large-scale sensitivity analysis or deep-surrogate
    training on supercomputers.
    This package builds the launcher and server modules.
    """

    homepage = "https://gitlab.inria.fr/melissa/melissa"
    git = "https://gitlab.inria.fr/melissa/melissa.git"
    maintainers("robcaulk", "mschouler", "raffino")

    version("develop", branch="develop")

    # define variants for the deep learning server (torch, tf)
    variant(
        "torch", default=False, description="Install Deep Learning requirements with Pytorch only"
    )
    variant(
        "tf", default=False, description="Install Deep Learning requirements with TensorFlow only"
    )

    depends_on("python@3.8.0:", type=("build", "run"))
    depends_on("py-setuptools@46.4:", type=("build"))
    # requirements.txt (SA)
    depends_on("py-pyzmq@22.3.0:", type="run")
    depends_on("py-mpi4py@3.1.3:", type="run")
    depends_on("py-numpy@1.21:", type="run")
    depends_on("py-jsonschema@4.5:", type="run")
    depends_on("py-python-rapidjson@1.8:", type="run")
    depends_on("py-scipy@1.10.0:", type="run")
    depends_on("py-cloudpickle@2.2.0:", type="run")
    # requirements_deep_learning.txt (DL with torch)
    depends_on("py-tensorboard@2.10.0:", type="run", when="+torch")
    depends_on("py-matplotlib", type="run", when="+torch")
    depends_on("py-torch@1.12.1:", type="run", when="+torch")
    # requirements_deep_learning.txt  (DL with tensorflow)
    depends_on("py-tensorboard@2.10.0:", type="run", when="+tf")
    depends_on("py-matplotlib", type="run", when="+tf")
    depends_on("py-tensorflow@2.8.0:", type="run", when="+tf")
