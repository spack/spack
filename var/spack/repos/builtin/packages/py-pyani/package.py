# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyani(PythonPackage):
    """pyani is a Python3 module that provides support for calculating
    average nucleotide identity (ANI) and related measures for whole genome
    comparisons, and rendering relevant graphical summary output. Where
    available, it takes advantage of multicore systems, and can integrate
    with SGE/OGE-type job schedulers for the sequence comparisons."""

    homepage = "https://widdowquinn.github.io/pyani"
    pypi = "pyani/pyani-0.2.7.tar.gz"

    license("MIT")

    version(
        "0.2.7",
        sha256="7516f6355fdfa0383eb85f5a9ec8ec865dd25499eb7874dd80344b1681898541",
        url="https://pypi.org/packages/d8/e0/bd5c359106506f82dfa6187ddb92d1f12e38a200e8c833dfd41ee37082eb/pyani-0.2.7-py3-none-any.whl",
    )
    version(
        "0.2.6",
        sha256="1abf33c8878f2a3602535ac5fcbf022e19acfe28942059f460cebf262cd8e570",
        url="https://pypi.org/packages/42/49/0dff571eff23353c69dd51b9c4934d5bc1b97b199cff5fd8eea7f7bb62ca/pyani-0.2.6-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-biopython", when="@0.1.3.2:")
        depends_on("py-matplotlib", when="@0.1.3.2:")
        depends_on("py-pandas", when="@0.1.3.2:")
        depends_on("py-scipy", when="@0.1.3.2:")
        depends_on("py-seaborn", when="@0.2.0.post:")

    # Required for ANI analysis

    # Required for ANIb analysis

    # Required for ANIm analysis
