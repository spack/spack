# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScreed(PythonPackage):
    """screed: a Python library for loading FASTA and FASTQ sequences."""

    homepage = "https://screed.readthedocs.io/"
    pypi = "screed/screed-1.1.2.tar.gz"

    version(
        "1.1.2",
        sha256="413e9cfce4b4908d0fa1fe69dcd2c523641a02a856eb196f9ce2183657f342dc",
        url="https://pypi.org/packages/a6/c1/e33d75369bffaf304b891afa34aa8b9765f117931673cdf8837eba9b0efb/screed-1.1.2-py2.py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@1.0.5:")
