# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMultiqc(PythonPackage):
    """MultiQC is a tool to aggregate bioinformatics results across many
    samples into a single report. It is written in Python and contains modules
    for a large number of common bioinformatics tools."""

    homepage = "https://multiqc.info"
    pypi = "multiqc/multiqc-1.0.tar.gz"

    license("GPL-3.0-only")

    version("1.15", sha256="ce5359a12226cf4ce372c6fdad142cfe2ae7501ffa97ac7aab544ced4db5ea3c")
    version("1.14", sha256="dcbba405f0c9521ed2bbd7e8f7a9200643047311c9619878b81d167300149362")
    version("1.13", sha256="0564fb0f894e6ca0822a0f860941b3ed2c33dce407395ac0c2103775d45cbfa0")

    depends_on("py-setuptools", type="build")
    depends_on("py-matplotlib@2.1.1:", type=("build", "run"))
    depends_on("py-networkx@2.5.1:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-click", type=("build", "run"))
    depends_on("py-coloredlogs", type=("build", "run"))
    depends_on("py-future@0.14.1:", type=("build", "run"))
    depends_on("py-jinja2@3.0.0:", type=("build", "run"), when="@1.14:")
    depends_on("py-jinja2@2.9:", type=("build", "run"), when="@:1.13")
    depends_on("py-lzstring", type=("build", "run"))
    depends_on("py-markdown", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-pyyaml@4:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-rich@10:", type=("build", "run"))
    depends_on("py-rich-click", type=("build", "run"))
    depends_on("py-simplejson", type=("build", "run"))
    depends_on("py-spectra@0.0.10:", type=("build", "run"))
    depends_on("py-spectra", type=("build", "run"))
