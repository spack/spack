# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.python import PythonPipBuilder
from spack.package import *


class Iotaa(PythonPackage):
    """A simple workflow engine with semantics inspired by Luigi
    and tasks expressed as decorated Python functions"""

    pypi = "iotaa/iotaa-1.2.3-py3-none-any.whl"

    maintainers("maddenp-noaa")

    license("Apache-2.0", checked_by="WeirAE")

    version("1.2.3", sha256="012d3c60b16ad4e245ac89b12b562283f91e310573f93b535ef747009085f480")
    version("1.2.2", sha256="e832288db712482aab86f618bad9e0820a9058ba35a9b25d6b34ff7ed90638c7")
    version("1.2.1", sha256="fb28a2bc943b4bc67f4103895d2590c130a295f2cc611b9bd0a49d3d24df8911")
    version("1.2.0", sha256="c51e23f568c831e954b9b97e8365a45b761024ae2146bdc8c80ff3a67e4bfb4a")
    version("1.1.6", sha256="4c379bdde08c6b1220b534599d0809ac9f17bb1bc30459f1512e7307498d3d82")
    version("1.1.5", sha256="f457c6ff1a709ad11b9d28cf0f24b095cfcb7a6ded2a48a09f95e3015b516435")
    version("1.1.4", sha256="9bb801e9b1edc7dac704bfe11b098c2c95a1dccdee84a4c7dbc5e9dcd20f0b84")
    version("1.1.3", sha256="bb56dcf3be000aaed1dec8e283d6c5d2f4e380c2abcf1a3934d4e98c7f9577a9")
    version("1.1.2", sha256="1a01fd805619a03eba4790bddaf2ea6e3255cded0efd8587ccd9e0463ef166ac")
    version("1.1.1", sha256="f890af8467c389e363ef4f18508b5ddb030167bb786f2aaaa81af3c35c41e41f")
    version("1.1.0", sha256="b998290a7442c7789517305e9ecc70b5cc6ab292dda8cd4a5ed27e29f05ff9e4")
    version("1.0.0", sha256="77919915274178b0f2748c4430444e845ffbce0b8b891d0808902412ef4996dd")
    version("0.8.3", sha256="63880c6454dc98a995be4fd7605b769d704248c38973d859884f01d16f4ee4e1")
    version("0.8.2", sha256="f755235c79e9eb2993f32e80409055f24a461fe99d4c093b681ea7e4626740cb")
    version("0.8.1", sha256="8dfbac33ab0e89b748790b9f7d22df2549dba3a781c0566e99a91083c537ef66")
    version("0.8.0", sha256="efb9f31dc39743fdee30ccf0d2ab8aec2d0e7e5748c452f79e12e746ccf2fe82")
    version("0.7.5", sha256="2ffe4d497a351e686f9302fb9ecdff3ec7cce5b22bcf980ec5d32dc56fa00cb4")
    version("0.7.4", sha256="b0fcd49d00908d5295c986df0960abb08c79fdc0652982e4cb5173cfd3656241")
    version("0.7.3", sha256="9b54aeab9639fa9b2413c7d029b0e5d41b118162e9911fa1cef9d88ee62cdcdc")
    version("0.7.2-1", sha256="b103f48b7b586285398b967401a268f72c79c9f9e97e5e31886faca8da75565d")

    depends_on("py-setuptools@42:", type="build")

    @property
    def build_wheel_file_path(self):
        wheel_file = f"#iotaa-{self.version}-py3-none-any.whl"
        wheel_dir = join_path("iotaa")
        return join_path(wheel_dir, wheel_file)

    def install(self, spec, prefix):
        whl = self.stage.archive_file
        python("-m", "pip", *PythonPipBuilder.std_args(self), f"--prefix={prefix}", whl)
