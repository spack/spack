# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGsd(PythonPackage):
    """The GSD file format is the native file format for HOOMD-blue. GSD files
    store trajectories of the HOOMD-blue system state in a binary file with
    efficient random access to frames. GSD allows all particle and topology
    properties to vary from one frame to the next. Use the GSD Python API to
    specify the initial condition for a HOOMD-blue simulation or analyze
    trajectory output with a script. Read a GSD trajectory with a visualization
    tool to explore the behavior of the simulation."""

    homepage = "https://gsd.readthedocs.io/en/stable/#"
    pypi = "gsd/gsd-1.9.3.tar.gz"

    maintainers("RMeli")

    version("2.8.0", sha256="f2b031a26a7a5bee5f3940dc2f36c5a5b6670307b297c526adf2e26c1f5b46ae")
    version("1.9.3", sha256="c6b37344e69020f69fda2b8d97f894cb41fd720840abeda682edd680d1cff838")

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@42:", type="build", when="@2.8.0:")
    depends_on("py-cython", type="build")
    depends_on("py-numpy@1.9.3:", type=("build", "run"))
    depends_on("py-numpy@1.9.3:1", when="@:1", type=("build", "run"))
