# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyContrib(PythonPackage):
    """A python package for making stacked area plots of contributions over time."""

    homepage = "https://github.com/spack/contrib"
    pypi = "contrib/contrib-0.3.0.tar.gz"

    license("Apache-2.0 OR MIT")

    version("0.3.0", sha256="55cf3a414c8b136f58588ec02e6833d1cc1d227a78f1778354ac6fcf9c2ccdda")

    with default_args(type=("build", "run")):
        depends_on("py-python-dateutil")
        depends_on("py-jsonschema")
        depends_on("py-matplotlib")
        depends_on("py-pyyaml")
        depends_on("py-setuptools")
