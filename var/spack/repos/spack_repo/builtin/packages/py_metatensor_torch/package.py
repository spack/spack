# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMetatensorTorch(PythonPackage):
    """TorchScript bindings for metatensor."""

    homepage = "https://docs.metatensor.org"
    url = "https://pypi.org/packages/source/m/metatensor-torch/metatensor_torch-0.7.6.tar.gz"

    import_modules = ["metatensor.torch"]

    maintainers("HaoZeke", "luthaf")
    license("BSD-3-Clause", checked_by="HaoZeke")

    version("0.7.6", sha256="bcc23b535e5b86c0d49096cbf73de67141896f4f14c114515d97b936a78353a1")
    version("0.7.5", sha256="d5180d90e9645d604d7e4817737298565d9d4a95aff7ad9e6407d3b9a5376b13")
    version("0.7.4", sha256="e317932c5a6cfd6fde42531ed8d9daae4f13f6ab2afe9bee86ad097887c906c8")
    version("0.7.3", sha256="20163f887852bf64c75404319ccf06751079d836db1dcc9343c843ba8e6b21de")
    version("0.7.2", sha256="2638b0c92d4cd547db199340c8a5fa2bf402ffe4fab541d1ae662dd82ae8b318")
    version("0.7.1", sha256="01ef652192bd5f857e9db4a7df21da45b5017e7ecd0ad6e46117d21e8535a090")
    version("0.7.0", sha256="6647632d68ed7dd0d651d977706394e26b23f037721380981be51caeef44d729")
    version("0.6.3", sha256="875f02b93ab9532f81c5f79d60d55007738ad9c450357aee20bcd4022be23acf")
    version("0.6.2", sha256="0d834683ccb11e73c42399694d0b94b299c3a7b63f0ba6fbb627709f068ff47a")
    version("0.6.1", sha256="f397888515c6eded84280c9c45c9d9c0ee12e76ccad2a1a0960888f643cce67a")
    version("0.6.0", sha256="5c8a3e7897f7b837551a0163d0d9326e9edcb61f4c78f443bc35e70c68381e14")
    version("0.5.5", sha256="a05bf20e0ec0937907c0145af83ebf9107df598caf9c9c36ca818ae7ead5f72d")
    version("0.5.4", sha256="fb45ab757da40fba464195b513b54da88179d0d1dfdf42ff83424d6c4e2202a1")
    version("0.5.3", sha256="7aef0fe12ab87f153b2763ab9d91ee29802f12122a0f3b3b6a649b2f6f09c703")
    version("0.5.2", sha256="379fcb9863d4ab9162fb182dcf09e25b44caf815186cbb7a70fcff075c13fa6f")
    version("0.5.1", sha256="722eebb94227769cb2b5d82599a60166c41c5dc986b772c2bb89323c717a0828")
    version("0.5.0", sha256="1242c14a7e581d21429ec4547ea5b34adbd80a8d2db092b13368761f9ae659e2")

    extends("python@3.9:")

    # Optional, XXX: to be declared upstream
    variant("torch", default=False, description="With PyTorch")
    variant("ase", default=False, description="With ASE")
    variant("operations", default=False, description="With added operations")
    variant("vesin", default=False, description="With added neighborlist functionality")
    variant("extended", default=False, description="With rascalaine, featomic and sphericart")

    # pyproject.toml
    depends_on("py-setuptools@77:", type="build")
    depends_on("py-packaging@23:", type="build")
    depends_on("cmake", type="build")
    depends_on("py-pip@22.1:", type="build")
    depends_on("py-torch@2.6:", type=("build", "run"), when="+torch")
    depends_on("vesin", type=("build", "run"), when="+vesin")

    depends_on("py-metatensor@0.1.13:", type="run")
    conflicts("py-metatensor@0.2.0:")
    # XXX: Needs to be declared upstream
    depends_on("py-numpy", type=("build", "run"))

    depends_on("libmetatensor-torch@0.7.6:", type="run")
    depends_on("py-metatensor@0.1.13:", type="run")
    conflicts("py-metatensor@0.2.0:")

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        env.set("METATENSOR_CORE_PYTHON_USE_EXTERNAL_LIB", "ON")
