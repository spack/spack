# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlit(PythonPackage):
    """Flit is a simple way to put Python packages and modules on PyPI."""

    homepage = "https://github.com/pypa/flit"
    pypi = "flit/flit-3.9.0.tar.gz"
    maintainers("takluyver")

    license("BSD-3-Clause")

    version("3.12.0", sha256="1c80f34dd96992e7758b40423d2809f48f640ca285d0b7821825e50745ec3740")
    version("3.11.0", sha256="58d0a07f684c315700c9c54a661a1130995798c3e495db0db53ce6e7d0121825")
    version("3.10.1", sha256="9c6258ae76d218ce60f9e39a43ca42006a3abcc5c44ea6bb2a1daa13857a8f1a")
    version("3.10.0", sha256="dadca58d5097db62884d25d70b572f104954927daadc8cee449739215b7237fd")
    version("3.9.0", sha256="d75edf5eb324da20d53570a6a6f87f51e606eee8384925cd66a90611140844c7")
    version("3.8.0", sha256="d0f2a8f4bd45dc794befbf5839ecc0fd3830d65a57bd52b5997542fac5d5e937")
    version("3.7.1", sha256="3c9bd9c140515bfe62dd938c6610d10d6efb9e35cc647fc614fe5fb3a5036682")
    version("3.6.0", sha256="b1464e006df4df4c8eeb37671c0e0ce66e1d04e4a36d91b702f180a25fde3c11")
    version("3.3.0", sha256="65fbe22aaa7f880b776b20814bd80b0afbf91d1f95b17235b608aa256325ce57")

    with default_args(type=("build", "run")):
        depends_on("python@3.8:", when="@3.10:")
        depends_on("python@3.6:")

        depends_on("py-flit-core@3.12.0:3", when="@3.12.0:3")
        depends_on("py-flit-core@3.11.0:3", when="@3.11.0:3")
        depends_on("py-flit-core@3.10.1:3", when="@3.10.1:3")
        depends_on("py-flit-core@3.10.0:3", when="@3.10.0:3")
        depends_on("py-flit-core@3.9.0:3", when="@3.9.0:3")
        depends_on("py-flit-core@3.8.0:3", when="@3.8.0:3.8")
        depends_on("py-flit-core@3.7.1:3", when="@3.7.1:3.7")
        depends_on("py-flit-core@3.6.0:3", when="@3.6.0:3.6")
        depends_on("py-flit-core@3.3.0:3", when="@3.3.0:3.3")

    with default_args(type=("run")):
        depends_on("py-pip", when="@3.10:")

        depends_on("py-requests")

        depends_on("py-docutils")

        depends_on("py-tomli", when="@3.4:3.7")
        depends_on("py-tomli-w", when="@3.4:")
        depends_on("py-toml", when="@3.3.0:3.3")
