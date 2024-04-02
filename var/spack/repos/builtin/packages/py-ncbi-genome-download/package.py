# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyNcbiGenomeDownload(PythonPackage):
    """Scripts to download genomes from the NCBI FTP servers"""

    homepage = "https://github.com/kblin/ncbi-genome-download/"
    pypi = "ncbi-genome-download/ncbi-genome-download-0.3.1.tar.gz"

    license("Apache-2.0")

    version(
        "0.3.1",
        sha256="5c28b83f4f53f4e45cb3bedc122dcdc99032377a8bb7e79f52e155bc5f6a2558",
        url="https://pypi.org/packages/0f/81/bb57c4450469c855926f55324bc09519f6625a58a17c4a1947f9f5938059/ncbi_genome_download-0.3.1-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-appdirs", when="@0.2.7:")
        depends_on("py-requests@2.4.3:")
        depends_on("py-tqdm", when="@0.3.1:")
