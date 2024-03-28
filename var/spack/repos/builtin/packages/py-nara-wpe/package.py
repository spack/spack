# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNaraWpe(PythonPackage):
    """Background noise and signal reverberation due to reflections in an
    enclosure are the two main impairments in acoustic signal processing and
    far-field speech recognition. This work addresses signal dereverberation
    techniques based on WPE for speech recognition and other far-field
    applications. WPE is a compelling algorithm to blindly dereverberate
    acoustic signals based on long-term linear prediction."""

    homepage = "https://github.com/fgnt/nara_wpe"
    pypi = "nara_wpe/nara_wpe-0.0.7.tar.gz"

    license("MIT")

    version(
        "0.0.7",
        sha256="ebcd08ad5f9050238d501e81eddcd6a73fc4669935d4f9677d72ee1ef3dfb7be",
        url="https://pypi.org/packages/4b/d4/11dddfd5f41017df8eda83cbcafab14ba8bf32d23e7697bf9d2bd343d979/nara_wpe-0.0.7-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-bottleneck")
        depends_on("py-click", when="@0.0.2:")
        depends_on("py-numpy")
        depends_on("py-soundfile")
        depends_on("py-tqdm")
