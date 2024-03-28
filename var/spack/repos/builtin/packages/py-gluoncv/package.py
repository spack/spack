# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGluoncv(PythonPackage):
    """GluonCV provides implementations of state-of-the-art
    (SOTA) deep learning algorithms in computer vision. It aims
    to help engineers, researchers, and students quickly
    prototype products, validate new ideas and learn computer
    vision."""

    homepage = "https://gluon-cv.mxnet.io/"
    pypi = "gluoncv/gluoncv-0.6.0.tar.gz"
    git = "https://github.com/dmlc/gluon-cv.git"

    license("Apache-2.0")

    version(
        "0.10.5.post0",
        sha256="93318cfda39ac3ac0fae3226f425f86b5edeafa581323e4f24927655538929ee",
        url="https://pypi.org/packages/8b/48/5564159e0ee638353bedfcdaf7a95f260d24969489444fab4cb01d1efe9d/gluoncv-0.10.5.post0-py2.py3-none-any.whl",
    )
    version(
        "0.6.0",
        sha256="7a169a546af47c2fa2aef41e772f5fc36710c48b3c4e51ef4dbe8cc7ad9d4288",
        url="https://pypi.org/packages/69/4d/d9d6b9261af8f7251977bb97be669a3908f72bdec9d3597e527712d384c2/gluoncv-0.6.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-autocfg", when="@0.9.0-beta20201105:")
        depends_on("py-autogluon-core", when="@0.9.0-beta20201105:0.10.1,0.11:0.11.0-beta20210605")
        depends_on("py-decord", when="@0.9.0-beta20201105:0.10.1,0.11:0.11.0-beta20210605")
        depends_on("py-matplotlib")
        depends_on("py-numpy")
        depends_on("py-opencv-python", when="@0.9.0-beta20201105:")
        depends_on("py-pandas", when="@0.9.0-beta20201105:")
        depends_on("py-pillow")
        depends_on("py-portalocker", when="@0.6.0-beta20191207:")
        depends_on("py-pyyaml", when="@0.9.0-beta20201105:")
        depends_on("py-requests")
        depends_on("py-scipy", when="@0.2:")
        depends_on("py-tensorboardx", when="@0.9.0-beta20201105:0.10.1,0.11:0.11.0-beta20210605")
        depends_on("py-tqdm")
        depends_on("py-yacs", when="@0.9.0-beta20201105:")
