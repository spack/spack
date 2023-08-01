# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyIbis(PythonPackage):
    """
    A Bayesian inference and sensitivity tool for building surrogate models 
    and performing uncertainity quantification analyses.
    """

    homepage = "https://github.com/LLNL/ibis"
    # url = "https://github.com/LLNL/ibis/archive/refs/tags/v1.0.0.tar.gz"
    pypi = "llnl-ibis/llnl_ibis-1.0.0.tar.gz"
    git = "https://github.com/LLNL/ibis"
    tags = ["v1.0.0"]


    # notify when the package is updated
    maintainers("sbeljurf")

    # git branches
    version("main", branch="main")

    # pypi releases
    version("1.0.0", sha256="44dcef4f900bdca439949a3e4d52f0b67320d6383a63253f24516a2d2072ca92", preferred=True)
    
    depends_on("py-setuptools", type=("build"))
    depends_on("py-poetry", type=("build"))

    with when("@3:"):
        depends_on("py-numpy", type=("build", "run"))
        depends_on("py-scipy", type=("build", "run"))
        depends_on("py-scikit-learn", type=("build", "run"))
        depends_on("py-matplotlib", type=("build", "run"))
        depends_on("py-networkx", type=("build", "run"))
        depends_on("py-trata", type=("build", "run"))
        