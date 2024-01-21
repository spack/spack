# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBiobbCommon(PythonPackage):
    """The base package required to use the biobb packages."""

    homepage = "https://biobb-common.readthedocs.io"
    pypi = "biobb_common/biobb_common-4.1.0.tar.gz"

    maintainers("w8jcik")

    version("4.1.0", sha256="97637f359a3bb8ad79aca72b6c26f73fe2424845dc7f43005643971046e9d117")

    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-biopython", type=("build", "run"))

    depends_on("py-setuptools", type="build")
