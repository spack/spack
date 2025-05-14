# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMetatensorOperations(PythonPackage):
    """Operations to manipulate metatensor data types."""

    homepage = "https://docs.metatensor.org"
    pypi = "metatensor-operations/metatensor_operations-0.3.3.tar.gz"

    import_modules = ["metatensor.operations"]

    maintainers("HaoZeke", "luthaf")
    license("BSD-3-Clause", checked_by="HaoZeke")

    version("0.3.3", sha256="432d267ce1f3c5ee11994d5348e70bc517a3c19ef68982af7bb470463e3c1b6b")
    version("0.3.2", sha256="90f815fc09632be9dd9176a89368fb7acc7c628f081201c2916220f61eb7a1af")
    version("0.3.1", sha256="715b34eb199232d005481a7c763e2f5ff69f23535cccaa9d4b07ca9977516b76")
    version("0.3.0", sha256="65aa60e9cbc98243bcb5bc3d7d89bae8400e3963be5fbcf1b5fbd7bec8b0b9b4")
    version("0.2.4", sha256="a93999596f28ac0d6c6c7e2c4a39de7cf25a9dd48c50dd4ba6f0b95a1b9f1124")
    version("0.2.3", sha256="409134773d0a59ff08e6b31ec24d1e5dcbb0f8fc8d1d2e94def10242de088122")
    version("0.2.2", sha256="64898aaf11d1ba7e9bdc48c25030839736b762c10c6cf6b2a3efad9c6f73988b")

    extends("python@3.9:")
    variant("torch", default=False, description="With PyTorch")

    # pyproject.toml
    depends_on("py-setuptools@77:", type="build")
    depends_on("py-packaging@23:", type="build")
    depends_on("py-pip@22.1:", type="build")
    depends_on("py-torch@2.6:", type=("build", "run"), when="+torch")
    depends_on("py-metatensor@0.1.10:", type="run")
    conflicts("py-metatensor@0.2.0:")
    # XXX: Needs to be declared upstream
    depends_on("py-numpy", type=("build", "run"))
