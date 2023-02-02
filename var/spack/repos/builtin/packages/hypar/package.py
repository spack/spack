# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hypar(AutotoolsPackage):
    """
    HyPar is a finite-difference algorithm to solve hyperbolic-parabolic partial differential
    equations (with source terms) on Cartesian grids. It is a unified framework that can handle
    systems of PDEs with arbitrary number of spatial dimensions and solution components. It
    provides the spatial discretization and time integration functions, functions to read and
    write solutions from/to files, as well as functions required to solve the system on parallel
    (MPI) platforms. The physical models define the physics-specific functions such as the exact
    forms of the hyperbolic flux, parabolic flux, source terms, upwinding functions, etc.
    """

    homepage = "http://hypar.github.io/"
    url = "https://bitbucket.org/deboghosh/hypar/get/v4.1.tar.gz"
    git = "https://bitbucket.org/deboghosh/hypar.git"

    maintainers("debog")

    tags = ["proxy-app", "ecp-proxy-app"]

    version("4.1", sha256="36c11dcfda006115f4656ff73790992e5caea99dbc64776c9db4e0a29b4c60da")

    variant("mpi", default=True, description="Build with MPI support")
    variant("openmp", default=False, description="Build with OpenMP support")
    variant("scalapack", default=False, description="Build with Scalapack Support")
    variant("fftw", default=False, description="Build with FFTW support")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    depends_on("mpi", when="+mpi")
    depends_on("scalapack", when="+scalapack")
    depends_on("blas", when="+scalapack")
    depends_on("lapack", when="+scalapack")
    depends_on("fftw", when="+fftw")

    patch_config_files = False

    def configure_args(self):
        args = []
        spec = self.spec
        if "+mpi" in spec:
            args.append("--enable-mpi")
            args.append("--with-mpi-dir={0}".format(spec["mpi"].prefix))
        if "+openmp" in spec:
            args.append("--enable-omp")
        if "+scalapack" in spec:
            args.append("--enable-scalapack")
            args.append("--with-blas-dir={0}".format(spec["blas"].prefix))
            args.append("--with-lapack-dir={0}".format(spec["lapack"].prefix))
            args.append("--with-scalapack-dir={0}".format(spec["scalapack"].prefix))
        if "+fftw" in spec:
            args.append("--enable-fftw")
            args.append("--with-fftw-dir={0}".format(spec["fftw"].prefix))
        return args
