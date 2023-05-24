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

    # define variants (DL, DL-Torch, DL-Tensorflow)
    variant(
        "MELISSA_DL",
        default=False,
        description="Install all Deep Learning requirements (Pytorch and TensorFlow)",
    )
    variant(
        "MELISSA_TORCH",
        default=False,
        description="Install Deep Learning requirements with Pytorch only",
    )
    variant(
        "MELISSA_TF",
        default=False,
        description="Install Deep Learning requirements with TensorFlow only",
    )

    depends_on("python@3.8.0:", type=("build", "run"))
    depends_on("py-setuptools", type=("build"))
    # requirements.txt (SA - note that plotext is not available with spack)
    depends_on("py-pyzmq@22.3.0:", type="run")
    depends_on("py-mpi4py@3.1.3:", type="run")
    depends_on("py-numpy@1.21:", type="run")
    depends_on("py-jsonschema@4.5:", type="run")
    depends_on("py-python-rapidjson@1.8:", type="run")
    depends_on("py-scipy@1.10.0:", type="run")
    depends_on("py-cloudpickle@2.2.0:", type="run")
    # requirements_deep_learning.txt (DL)
    depends_on("py-tensorboard@2.10.0:", type="run", when="+MELISSA_DL")
    depends_on("py-matplotlib", type="run", when="+MELISSA_DL")
    depends_on("py-torch@1.13.0:", type="run", when="+MELISSA_DL")
    depends_on("py-tensorflow@2.8.0:", type="run", when="+MELISSA_DL")
    # variant scpeficic dependencies (TORCH)
    depends_on("py-tensorboard@2.10.0:", type="run", when="+MELISSA_TORCH")
    depends_on("py-matplotlib", type="run", when="+MELISSA_TORCH")
    depends_on("py-torch@1.13.0:", type="run", when="+MELISSA_TORCH")
    # variant scpeficic dependencies (TF)
    depends_on("py-tensorboard@2.10.0:", type="run", when="+MELISSA_TF")
    depends_on("py-matplotlib", type="run", when="+MELISSA_TF")
    depends_on("py-tensorflow@2.8.0:", type="run", when="+MELISSA_TF")
