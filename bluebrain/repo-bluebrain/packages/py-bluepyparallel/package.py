# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBluepyparallel(PythonPackage):
    """Python library to run embarassingly parallel computations."""

    homepage = "https://bbpgitlab.epfl.ch/neuromath/bluepyparallel"
    git = "ssh://git@bbpgitlab.epfl.ch/neuromath/bluepyparallel.git"

    version("0.2.0", tag="bluepyparallel-v0.2.0")
    version("0.0.9", tag="bluepyparallel-v0.0.9")
    version("0.0.5", tag="BluePyParallel-v0.0.5")

    depends_on("py-setuptools", type="build")

    depends_on("py-pandas@0.24:", type="run", when="@:0.0.5")
    depends_on("py-pandas@1.3:", type="run", when="@0.0.8:")
    depends_on("py-dask+dataframe+distributed@2.30:", type="run", when="@:0.0.5")
    depends_on("py-dask+dataframe+distributed@2021.11:", type="run", when="@0.0.8:")
    depends_on("py-dask-mpi@2.21.0:", type="run", when="@:0.0.5")
    depends_on("py-dask-mpi@2021.11:", type="run", when="@0.0.8:")
    depends_on("py-mpi4py@3.0.3:", type="run")
    depends_on("py-tqdm@4.28.1:", type="run")
    depends_on("py-sqlalchemy@:1.3", type="run", when="@:0.0.5")
    depends_on("py-sqlalchemy@:1.4", type="run", when="@0.0.8:")
    depends_on("py-sqlalchemy-utils@0.36:", type="run", when="@:0.0.5")
    depends_on("py-sqlalchemy-utils@0.37.2:", type="run", when="@0.0.8:")
    depends_on("py-ipyparallel@6.3:6", type="run", when="@0.0.8:0.1")
    depends_on("py-ipyparallel@6.3:", type="run", when="@0.2.0:")
