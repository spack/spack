# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyDistlib(PythonPackage):
    """Distribution utilities"""

    homepage = "https://github.com/pypa/distlib"
    pypi = "distlib/distlib-0.3.6.tar.gz"

    license("PSF-2.0")

    version("0.3.9", sha256="a60f20dea646b8a33f3e7772f74dc0b2d0772d2837ee1342a00645c81edf9403")
    version("0.3.8", sha256="1530ea13e350031b6312d8580ddb6b27a104275a31106523b8f123787f494f64")
    version("0.3.7", sha256="9dafe54b34a028eafd95039d5e5d4851a13734540f1331060d31c9916e7147a8")
    version("0.3.6", sha256="14bad2d9b04d3a36127ac97f30b12a19268f211063d8f8ee4f47108896e11b46")
    version("0.3.4", sha256="e4b58818180336dc9c529bfb9a0b58728ffc09ad92027a3f30b7cd91e3458579")
    version("0.3.3", sha256="d982d0751ff6eaaab5e2ec8e691d949ee80eddf01a62eaa96ddb11531fe16b05")

    depends_on("c", type="build")  # generated

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@44:", when="@0.3.6:", type="build")
    depends_on("py-wheel@0.29.0:", when="@0.3.6:", type="build")

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/d/distlib/distlib-{0}.{1}"
        if version >= Version("0.3.5"):
            ext = "tar.gz"
        else:
            ext = "zip"
        return url.format(version, ext)
