# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install iotaa
#
# You can edit this file again by typing:
#
#     spack edit iotaa
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Iotaa(PythonPackage):
    """A simple workflow engine with semantics inspired by Luigi and tasks expressed as decorated Python functions"""

    pypi = "iotaa/#iotaa-1.1.6-py3-none-any.whl"

    maintainers("maddenp-noaa")

    license("Apache-2.0", checked_by="WeirAE")

    version("1.1.6-0", sha256="b375edafec7dc00f854f7122e0817924ce53f05e0a62e01422ea44aff25c5f8d")

    depends_on("py-setuptools@42:", type="build")

    @property
    def build_wheel_file_path(self):
        wheel_file = f"#iotaa-{self.version}-py3-none-any.whl"
        wheel_dir = join_path("iotaa")
        return join_path(wheel_dir, wheel_file)

    def install(self, spec, prefix):
        spec = self.spec
        pip = which("pip")
        wheel = self.build_wheel_file_path

        # This mimics the install-on-cluster target but avoids anything
        # that utilizes pip to resolve dependencies
        with working_dir(join_path(self.stage.source_path, "iotaa")):
            pip("install", f"--prefix={prefix}", wheel)