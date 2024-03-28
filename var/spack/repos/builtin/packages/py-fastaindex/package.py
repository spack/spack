# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFastaindex(PythonPackage):
    """FastA index (.fai) handler compatible with samtools faidx is extended
    with 4 columns storing counts for A, C, G & T for each sequence.."""

    homepage = "https://github.com/lpryszcz/FastaIndex"
    pypi = "FastaIndex/FastaIndex-0.11rc7.tar.gz"

    license("GPL-3.0-or-later")

    version(
        "0.11-rc7",
        sha256="2f7fa2c86c39b11a9a8c545ed1cd9d9bc16faa3758dfdebe800766ab41e04132",
        url="https://pypi.org/packages/ee/24/2da46550b77abc0a546deb81a8a43df403a0ae224ed052081eea0fc4a57d/FastaIndex-0.11rc7-py2-none-any.whl",
    )
