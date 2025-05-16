# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.python import PythonPipBuilder
from spack.package import *


class Iotaa(PythonPackage):
    """A simple workflow engine with semantics inspired by Luigi
    and tasks expressed as decorated Python functions"""

    homepage = "https://github.com/maddenp/iotaa"
    pypi = "iotaa/iotaa-1.2.3-py3-none-any.whl"

    maintainers("maddenp")

    license("Apache-2.0", checked_by="WeirAE")

    version(
        "1.2.3",
        sha256="012d3c60b16ad4e245ac89b12b562283f91e310573f93b535ef747009085f480",
        url="https://files.pythonhosted.org/packages/25/b7/79e5122ec05d69063da576d0732bbdf48e850f2b8bcbc3e7e30f688dd1a6/iotaa-1.2.3-py3-none-any.whl",
        expand=False,
    )
    version(
        "1.1.6",
        sha256="4c379bdde08c6b1220b534599d0809ac9f17bb1bc30459f1512e7307498d3d82",
        url="https://files.pythonhosted.org/packages/0b/46/e3ba60b9bf0657774ce83d38ca569e9f1fc551ce9aa6fa5af3faa9ee9ce5/iotaa-1.1.6-py3-none-any.whl",
        expand=False,
    )
    version(
        "0.8.3",
        sha256="63880c6454dc98a995be4fd7605b769d704248c38973d859884f01d16f4ee4e1",
        url="https://files.pythonhosted.org/packages/95/74/2a604d536a10b009c3b46db34dc02dd26893749aaf3cc54522c2d7d87d9c/iotaa-0.8.3-py3-none-any.whl",
        expand=False,
    )

    depends_on("py-setuptools@42:", type="build")

    @property
    def build_wheel_file_path(self):
        wheel_file = f"#iotaa-{self.version}-py3-none-any.whl"
        wheel_dir = join_path("iotaa")
        return join_path(wheel_dir, wheel_file)

    def install(self, spec, prefix):
        whl = self.stage.archive_file
        python("-m", "pip", *PythonPipBuilder.std_args(self), f"--prefix={prefix}", whl)
