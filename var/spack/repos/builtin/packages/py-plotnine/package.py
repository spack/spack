# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.directives import depends_on, version


class PyPlotnine(PythonPackage):
    """plotnine is an implementation of a grammar of graphics in Python, it is
    based on ggplot2. The grammar allows users to compose plots by explicitly
    mapping data to the visual objects that make up the plot."""

    pypi = "plotnine/plotnine-0.8.0.tar.gz"

    version(
        "0.8.0",
        sha256="39de59edcc28106761b65238647d0b1f6212ea7f3a78f8be0b846616db969276",
    )

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on("py-descartes@1.1.0:", type=("build", "run"))
    depends_on("py-matplotlib@3.1.1:", type=("build", "run"))
    depends_on("py-mizani@0.7.3:", type=("build", "run"))
    depends_on("py-numpy@1.19.0:", type=("build", "run"))
    depends_on("py-pandas@1.1.0:", type=("build", "run"))
    depends_on("py-patsy@0.5.1:", type=("build", "run"))
    depends_on("py-scipy@1.5.0:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-statsmodels@0.12.1:", type=("build", "run"))
