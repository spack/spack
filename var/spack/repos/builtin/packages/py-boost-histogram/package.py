# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBoostHistogram(PythonPackage):
    """The Boost::Histogram Python wrapper."""

    homepage = "https://github.com/scikit-hep/boost-histogram"
    pypi = "boost_histogram/boost_histogram-1.2.1.tar.gz"

    version("1.3.1", sha256="31cd396656f3a37834e07d304cdb84d9906bc2172626a3d92fe577d08bcf410f")
    version("1.2.1", sha256="a27842b2f1cfecc509382da2b25b03056354696482b38ec3c0220af0fc9b7579")

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-setuptools@45:", type="build")
    depends_on("py-setuptools-scm@4.1.2:+toml", type="build")
    depends_on("py-numpy@1.13.3:", type=("build", "run"))
    depends_on("py-typing-extensions", when="^python@:3.7", type=("build", "run"))
