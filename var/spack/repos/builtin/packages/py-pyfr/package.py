# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyPyfr(PythonPackage):
    """PyFR is an open-source Python based framework for solving
    advection-diffusion type problems on streaming architectures
    using the Flux Reconstruction approach of Huynh."""

    homepage = "http://www.pyfr.org/"
    pypi = "pyfr/pyfr-1.13.0.tar.gz"
    git = "https://github.com/PyFR/PyFR/"
    maintainers = ["MichaelLaufer"]

    # git branches
    version("develop", branch="develop")
    version("master", branch="master")

    # pypi releases
    version(
        "1.14.0",
        sha256="ebf40ce0896cce9ac802e03fd9430b5be30ea837c31224531a6d5fd68f820766",
    )
    version(
        "1.13.0",
        sha256="ac6ecec738d4e23799ab8c50dea9bdbd7d37bc971bd33f22720c5a230b8e7b2f",
    )

    variant("metis", default=True, description="Metis for mesh partitioning")
    variant("scotch", default=False, description="Scotch for mesh partitioning")
    variant("cuda", default=False, description="CUDA backend support")
    variant("hip", default=False, description="HIP backend support")
    variant("libxsmm", default=True, description="LIBXSMM for OpenMP backend")
    variant("scipy", default=True, description="Scipy acceleration for point sampling")

    # Required dependencies
    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-gimmik@2.2:2", type=('build', 'run'))
    depends_on("py-gimmik@2.3:2", when='@1.14.0:', type=('build', 'run'))
    depends_on("py-h5py@2.10:", type=('build', 'run'))
    depends_on("py-mako@1.0.0:", type=('build', 'run'))
    depends_on("py-mpi4py@3.1.0:", type=('build', 'run'))
    depends_on("py-numpy@1.20:+blas", type=('build', 'run'))
    depends_on("py-platformdirs@2.2.0:", type=('build', 'run'))
    depends_on("py-pytools@2016.2.1:", type=('build', 'run'))

    # Optional dependencies
    depends_on("py-scipy", when="+scipy", type=('build', 'run'))
    depends_on("scotch@6.0:", when="+scotch", type=('run'))
    depends_on("cuda@8.0:", when="+cuda", type=('run'))
    depends_on("rocblas@4.5.0:", when="+hip", type=('run'))
    depends_on("libxsmm@1.18:+shared blas=0 +large_jit_buffer", when="+libxsmm", type=('run'))
