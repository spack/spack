# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVesin(PythonPackage):
    """Computing neighbor lists for atomistic system."""

    homepage = "https://luthaf.fr/vesin/latest/index.html"
    pypi = "vesin/vesin-0.3.7.tar.gz"

    import_modules = ["vesin"]

    maintainers("HaoZeke", "luthaf")
    license("BSD-3-Clause", checked_by="HaoZeke")

    version("0.3.7", sha256="52c11ac0ba775c228f06779877cf8641854edab7ea59036093ef5e8447379de0")
    version("0.3.6", sha256="70f1af8483f6197a009ffa425ed424ecde050187d5a07e83cb811025f62adfc9")
    version("0.3.5", sha256="1ad9a6bcd44d4313e8e2ce81ed58aa23f37e7d4cebd9570323c98086a3c41902")
    version("0.3.4", sha256="75969ffe61ece56ce415b70b2ca2b5b948a9a0be5f3a9a4e38f9092f118de43a")
    version("0.3.3", sha256="4a3685959e6a7b416f0347afcd99896c299a8a8430f815f91c499b062e135754")
    version("0.3.2", sha256="7fc156d2475eca763534a08f7e91d153c707c209bc10e8d081276b4338eb2d5a")
    version("0.3.1", sha256="31544727118968f6e8e50b3536eba7695c12ad92e2932141fd1b40e7a032ee6e")
    version("0.3.0", sha256="bb325eb9f41e6632600379b1babd26264859d68b2bd1a8bff22ef23efbd8a689")
    version("0.2.0", sha256="7c49e11aa46c06ae8e3154d52b462ae0e19aa090eda4b226b7fd5a4e35e87a30")
    version("0.1.0", sha256="019a71707202e1bd9e6e833bb8cf0fc21c2b60565ac8a4a9a6b05d61527855d9")

    extends("python@3.9:")

    # Optional, XXX: to be declared upstream
    variant("ase", default=False, description="With ASE")
    variant("metatensor", default=False, description="With metatensor learn, torch")
    variant("metatomic", default=False, description="With metatomic")
    variant("torch", default=False, description="With PyTorch")

    # pyproject.toml
    depends_on("py-numpy")
    depends_on("ase", type=("build", "run"), when="+ase")
    depends_on("py-torch@2.6:", type=("build", "run"), when="+torch")

    depends_on("py-setuptools@77:", type="build")
    depends_on("py-wheel@0.41:", type="build")
    depends_on("py-packaging@23:", type="build")
    depends_on("cmake", type="build")

    depends_on("py-pip@22.1:", type="build")
