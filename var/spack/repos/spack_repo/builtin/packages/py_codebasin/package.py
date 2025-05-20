# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyCodebasin(PythonPackage):
    """An analysis tool providing insight into the portability and
    maintainability of an application's source code."""

    homepage = "https://intel.github.io/code-base-investigator/"

    url = "https://github.com/intel/code-base-investigator/archive/refs/tags/2.0.0.tar.gz"

    maintainers("pennycook")

    license("BSD-3-Clause", checked_by="pennycook")

    version("2.0.0", sha256="f19af5418ab470f1cc22a503f24526ecc7de947f4cdcf897b9c1189d5d97d8e9")

    depends_on("cxx", type="build")
    depends_on("fortran", type="build")

    depends_on("python@3.12:", type=("build", "run"))

    depends_on("py-setuptools@64:", type="build")
    depends_on("py-setuptools-scm@8:", type="build")

    with default_args(type=("build", "run")):
        depends_on("py-numpy@2.2.4")
        depends_on("py-matplotlib@3.10.1")
        depends_on("py-pathspec@0.12.1")
        depends_on("py-scipy@1.15.2")
        depends_on("py-jsonschema@4.23.0")
        depends_on("py-tabulate@0.9.0")
        depends_on("py-tqdm@4.67.1")
