# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVarifier(PythonPackage):
    """Variant call verification"""

    homepage = "https://github.com/iqbal-lab-org/varifier"
    pypi = "varifier/varifier-0.3.1.tar.gz"
    git = "https://github.com/iqbal-lab-org/varifier"

    version("master", branch="master")
    version("0.3.1", sha256="74d0da83508b0ffd2c838d0cd6dc59db244df0bd50fce5271a8d7e01a0a931f1")
    version("0.2.0", sha256="e2fe7b59544a7cd2e60a709839040d030a3044827d50abb05bccb4cd8ae47300")
    version("0.1.0", sha256="c722ffb8d0362ca0a10e41e4fb350ef10ed11d21b099ec79b723325e508082fd")

    depends_on("py-setuptools", type="build")
    depends_on("bcftools", type="run")
    depends_on("vt", type="run")
    depends_on("py-biopython", type=("build", "run"))
    depends_on("py-cluster-vcf-records@0.13.2:", type=("build", "run"))
    # mappy >= 2.17 provided by minimap2
    depends_on("minimap2@2.17:", type=("build", "run"))
    depends_on("py-pandas")
    depends_on("py-pyfastaq@3.14.0:")
    depends_on("py-pymummer")
    depends_on("py-pysam", type="run")
    depends_on("py-seaborn", type=("build", "run"))

    @run_before("install")
    def configure(self):
        filter_file(', "k8"', "", "varifier/truth_variant_finding.py")
