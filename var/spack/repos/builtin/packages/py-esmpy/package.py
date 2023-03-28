# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEsmpy(PythonPackage):
    """ESMPy is a Python interface to the Earth System Modeling Framework (ESMF)"""

    homepage = "https://earthsystemmodeling.org/"
    url = "https://github.com/esmf-org/esmf/archive/refs/tags/v8.4.0.tar.gz"
    git = "https://github.com/esmf-org/esmf.git"

    version("develop", branch="develop")
    version("8.4.0", sha256="28531810bf1ae78646cda6494a53d455d194400f19dccd13d6361871de42ed0f")
    version("8.3.1", sha256="6c39261e55dcdf9781cdfa344417b9606f7f961889d5ec626150f992f04f146d")
    version("8.3.0", sha256="0ff43ede83d1ac6beabd3d5e2a646f7574174b28a48d1b9f2c318a054ba268fd")
    version("8.2.0", sha256="3693987aba2c8ae8af67a0e222bea4099a48afe09b8d3d334106f9d7fc311485")
    version("8.1.1", sha256="58c2e739356f21a1b32673aa17a713d3c4af9d45d572f4ba9168c357d586dc75")
    version("8.0.1", sha256="9172fb73f3fe95c8188d889ee72fdadb4f978b1d969e1d8e401e8d106def1d84")
    version("8.0.0", sha256="051dca45f9803d7e415c0ea146df15ce487fb55f0fce18ca61d96d4dba0c8774")

    maintainers("angus-g")

    # require an in-sync version of ESMF
    for v in ["develop", "8.4.0", "8.3.1", "8.3.0", "8.2.0", "8.1.1", "8.0.1", "8.0.0"]:
        depends_on(f"esmf@{v}", when=f"@{v}", type=("build", "run"))

    depends_on("py-setuptools@41:", type="build")
    depends_on("py-build", when="@:8.3.1", type="build")
    depends_on("py-setuptools-git-versioning", when="@8.4.0: ^python@3.10:", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-importlib-metadata", when="@8.4.0: ^python@:3.7")

    patch("setuppy.patch", when="@:8.3.1")

    @property
    def build_directory(self):
        if self.version < Version("8.4.0"):
            return join_path("src", "addon", "ESMPy")

        return join_path("src", "addon", "esmpy")

    def url_for_version(self, version):
        if version < Version("8.2.1"):
            return "https://github.com/esmf-org/esmf/archive/ESMF_{0}.tar.gz".format(
                version.underscored
            )
        else:
            # Starting with ESMF 8.2.1 releases are now in the form vx.y.z
            return "https://github.com/esmf-org/esmf/archive/refs/tags/v{0}.tar.gz".format(
                version.dotted
            )
