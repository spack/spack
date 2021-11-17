# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.python import PythonPackage
from spack.directives import depends_on, variant, version


class PyAtlinter(PythonPackage):
    """Interpolation of section images."""

    homepage = "https://atlas-interpolation.rtfd.io"
    git = "git@bbpgitlab.epfl.ch:project/proj101/atlas_interpolation.git"

    maintainers = ["EmilieDel", "Stannislav"]

    version(
        "0.2.3",
        url="https://files.pythonhosted.org/packages/57/d3/4cdfaacccff677b32687cbcfd689727bc7b3a8f4485401aa3eca157e5aaf/atlinter-0.2.3.tar.gz",
        sha256="67f102b70bc7eeb450da8af3c19df38610dd081a025f9c04e8f5266d2d0cc6e3",
    )
    version("0.2.2", tag="v0.2.2")
    version("0.2.1", tag="v0.2.1")
    version("0.2.0", tag="v0.2.0")
    version("0.1.1", tag="v0.1.1")
    version("0.1.0", tag="v0.1.0")

    variant("cuda", default=False, description="Enable CUDA support")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")

    # opencv leads to problems:
    # fatal error: opencv2/opencv.hpp: No such file or directory
    depends_on("mxnet+cuda~opencv", when="@0.1.1:+cuda", type=("build", "run"))
    depends_on("mxnet~cuda~opencv", when="@0.1.1:~cuda", type=("build", "run"))
    depends_on("py-atlannot", when="@0.2.2:", type=("build", "run"))
    depends_on("py-atldld@0.2.2", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pillow", type=("build", "run"))
    depends_on("py-pytorch-fid", type=("build", "run"))
    depends_on("py-pynrrd", when="@0.2.2:", type=("build", "run"))
    depends_on("py-pyyaml", when="@0.1.1:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-scikit-image", when="@0.2.2:", type=("build", "run"))
    depends_on("py-scipy", when="@0.1.1:", type=("build", "run"))
    depends_on("py-torch+cuda", when="+cuda", type=("build", "run"))
    depends_on("py-torch~cuda~cudnn~nccl", when="~cuda", type=("build", "run"))
    depends_on("py-torchvision", type=("build", "run"))
