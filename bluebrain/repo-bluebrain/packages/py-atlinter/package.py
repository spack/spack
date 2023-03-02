# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.python import PythonPackage
from spack.directives import depends_on, variant, version


class PyAtlinter(PythonPackage):
    """Interpolation of section images."""

    homepage = "https://atlas-interpolation.rtfd.io"
    git = "https://github.com/BlueBrain/atlas-interpolation.git"

    maintainers = ["EmilieDel", "Stannislav"]

    version("0.2.4", tag="v0.2.4")

    variant("cuda", default=False, description="Enable CUDA support")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")

    # opencv leads to problems:
    # fatal error: opencv2/opencv.hpp: No such file or directory
    # mxnet is pinned because otherwise it tries to build @1.master.
    depends_on("mxnet@1.8+cuda~opencv", when="+cuda", type=("build", "run"))
    depends_on("mxnet@1.8~cuda~opencv", when="~cuda", type=("build", "run"))
    depends_on("py-atlannot", type=("build", "run"))
    depends_on("py-atldld@0.2.2", type=("build", "run"))
    depends_on("py-dvc+ssh", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pillow", type=("build", "run"))
    depends_on("py-pytorch-fid+cuda", when="+cuda", type=("build", "run"))
    depends_on("py-pytorch-fid~cuda", when="~cuda", type=("build", "run"))
    depends_on("py-pynrrd", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-scikit-image", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-torch+cuda", when="+cuda", type=("build", "run"))
    depends_on("py-torch~cuda", when="~cuda", type=("build", "run"))
    # force newer version to force newer py-torch
    # py-torchvision is pretty strict about what py-torch it wants,
    # so just setting py-torch@... is not enough
    depends_on("py-torchvision@0.14:", type=("build", "run"))
