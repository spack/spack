# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHeat(PythonPackage):
    """Heat is a flexible and seamless open-source software for high performance data analytics
    and machine learning. It provides highly optimized algorithms and data structures for tensor
    computations using CPUs, GPUs and distributed cluster systems on top of MPI."""

    homepage = "https://github.com/helmholtz-analytics/heat/"
    pypi = "heat/heat-1.3.0.tar.gz"

    maintainers("mrfh92", "ClaudiaComito", "JuanPedroGHM")

    license("MIT")

    version(
        "1.3.0",
        sha256="d0551ca2a8cedb9c05002c076b747d85a5fd294c6bd63f5e390df1272eaaa6a3",
        url="https://pypi.org/packages/a6/b9/3d9dd4940b0a5b2f1ef81f982a4d608614c3e062cd079f12b0c342f36992/heat-1.3.0-py3-none-any.whl",
    )

    variant("dev", default=False, description="Use the py-pre-commit package")
    variant("docutils", default=False, description="Use the py-docutils package")
    variant(
        "examples",
        default=False,
        description="Use py-scikit-learn and py-matplotlib for the example tests",
    )
    variant("hdf5", default=False, description="Use the py-h5py package needed for HDF5 support")
    variant(
        "netcdf", default=False, description="Use the py-netcdf4 package needed for NetCDF support"
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@1.3:")
        depends_on("py-docutils@0.16:", when="@1:+docutils")
        depends_on("py-h5py@2.8.0:", when="@0.4:+hdf5")
        depends_on("py-matplotlib@3.1.0:", when="@1.2:+examples")
        depends_on("py-mpi4py@3:", when="@0.4:")
        depends_on("py-netcdf4@1.5.6:", when="@1:+netcdf")
        depends_on("py-numpy@1.20.0:", when="@1.3:")
        depends_on("py-pillow@6:", when="@1:")
        depends_on("py-pre-commit@1.18.3:", when="@0.4:+dev")
        depends_on("py-scikit-learn@0.24.0:", when="@1.2:+examples")
        depends_on("py-scipy@0.14:", when="@0.5:")
        depends_on("py-torch@1.8:2.0", when="@1.3:")
        depends_on("py-torchvision@0.8:", when="@1:1.1.0,1.2:")
