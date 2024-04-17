# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHepstats(Package):
    """hepstats is a library for statistical inference aiming
    to cover the needs High Energy Physics.
    It is part of the Scikit-HEP project.
    """

    homepage = "https://github.com/scikit-hep/hepstats"
    pypi = "hepstats/hepstats-0.8.0.tar.gz"

    maintainers("jonas-eschle")

    license("BSD-3-Clause", checked_by="jonas-eschle")

    tags = ["likelihood", "statistics", "inference", "fitting", "hep"]

    version("0.8.1", sha256="78f283fc77b2a1bd0f6dd108f2ecce269359a14797cbf3a1af2eea9a29ce96db")

    depends_on("python@3.9:3.12", type=("build", "run"), when="@0.8:")
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm@3.4:+toml", type="build")

    variant("zfit", default=True, description="Allows to use improved tools from zfit.")

    with default_args(type=("build", "run")):
        depends_on("py-pandas")
        depends_on("py-numpy")
        depends_on("py-asdf")
        depends_on("py-scipy")
        depends_on("py-tqdm")
        depends_on("py-uhi")

        with when("+zfit"):
            depends_on("py-zfit@0.20", when="@0.8:")
