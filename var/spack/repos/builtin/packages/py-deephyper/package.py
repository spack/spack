# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDeephyper(PythonPackage):
    """Scalable asynchronous neural architecture and hyperparameter
    search for deep neural networks."""

    homepage = "https://deephyper.readthedocs.io/"
    pypi = "deephyper/deephyper-0.4.2.tar.gz"
    git = "https://github.com/deephyper/deephyper.git"

    maintainers("mdorier", "Deathn0t")

    license("BSD-3-Clause")

    version(
        "0.4.2",
        sha256="a677202e0ed32d928541035b1ffce485ad0d701f5ecc9e9a4ae3350f7b8d3d6c",
        url="https://pypi.org/packages/4d/ce/600ba9d8be4eb6c2896e98b858f12c07d829afb37f192455ac766b8e0a18/deephyper-0.4.2-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:3.9", when="@0.3.3:0.4")
        depends_on("py-configspace@0.4.20:", when="@0.4:")
        depends_on("py-dm-tree", when="@0.4:")
        depends_on("py-jinja2@:3.0", when="@0.4:")
        depends_on("py-numpy", when="@0.2.5:0.5")
        depends_on("py-packaging", when="@0.4:")
        depends_on("py-pandas@0.24.2:")
        depends_on("py-pyyaml", when="@0.4:")
        depends_on("py-scikit-learn@0.23.1:")
        depends_on("py-scipy@0.19.1:", when="@0.4")
        depends_on("py-tinydb", when="@0.4")
        depends_on("py-tqdm@4.64:", when="@0.4:")
