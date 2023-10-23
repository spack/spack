# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyClusterVcfRecords(PythonPackage):
    """Python package to cluster VCF records. Used by gramtools and minos"""

    homepage = "https://github.com/iqbal-lab-org/cluster_vcf_records"

    pypi = "cluster-vcf-records/cluster_vcf_records-0.13.3.tar.gz"

    version("0.13.3", sha256="dc8a2f55a4d58159c3152195441c8821abdbe430fc8b529c0d22a1ebda26d58c")
    version("0.13.2", sha256="ba587de2a5b8330d9cd4ae904f926eb7af6585f340fba45e3c90b37d9a2045b1")
    version("0.13.1", sha256="4fb16ae3c8495168c911adc51e9d33fad385995ab69e1b41d3ba4ab3e6ab1d35")
    version("0.13.0", sha256="c863a0415b5a071fafd88b21d6b378fb96cf478ee73a5dafecd5b8f25c6dbb7a")
    version("0.12.4", sha256="116032bab09c2205ad7fba47e6181b52a383973d6d065e207046de56ce347fa9")
    version("0.12.3", sha256="45f02153262b1020959180d08893ad50aa80e1b6a72b14a716e6c19bae5cde12")
    version("0.12.2", sha256="10741b6c0f96aa55415b4125008fdfe14d6084705a19f96a2365806328e7eb65")
    version("0.12.1", sha256="d8d8d4585a41e375bc53406e6400805c3c1da2a88c96d4d7c00ed55ac1277e88")
    version("0.12.0", sha256="3871924d34ab1da01e4ffebdc9240679eff7d4e9fd9249b701db5042c4c46432")
    version("0.11.1", sha256="49140120a495a15cb503c6e0136a2875507b927c6bd11df498be0a100058f5cb")
    version("0.11.0", sha256="5739559ca9e450e3561a6d44d09c92c5c8fbd877aae80a6ce5cf180a0ef13e97")

    depends_on("py-setuptools", type="build")
    depends_on("py-bitarray", type=("build", "run"))
    depends_on("py-pyfastaq@3.14.0:", type=("build", "run"))
    depends_on("py-pysam", type=("build", "run"))
    depends_on("bcftools", type="run")
    depends_on("vt", type="run")
