# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

class PyNanoget(PythonPackage):
    """Functions to extract information from Oxford Nanopore sequencing data and alignments"""

    homepage = "https://github.com/wdecoster/nanoget"
    pypi = "nanoget/nanoget-1.19.3.tar.gz"

    maintainers("Pandapip1")

    version("1.19.3", sha256="da981810edb1cbe42cbbfbe5fcf753f29bf5555204cd51256b28a284a036a71b")

    depends_on("python@3")
    depends_on("py-biopython")
    depends_on("py-pysam@0.10.0.0:")
    depends_on("py-pandas@2.0.0:")
    depends_on("py-numpy")
