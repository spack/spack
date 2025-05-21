# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyOdcGeo(PythonPackage):
    """Geometry Classes and Operations (opendatacube)."""

    homepage = "https://github.com/opendatacube/odc-geo/"
    pypi = "odc-geo/odc_geo-0.1.2.tar.gz"

    license("Apache-2.0")

    version("0.4.10", sha256="5670a797c4243e9379b20905ea37ff23ad287e7fa37c672dc53546923daf6d52")
    version("0.1.2", sha256="c5ec3c66a326b138df5a28aa639b1c2c3c644093af463948255219bdc2513408")

    depends_on("py-setuptools@51:", type="build")

    with default_args(type=("build", "run")):
        depends_on("py-affine")
        depends_on("py-cachetools")
        depends_on("py-numpy")
        depends_on("py-pyproj@3:", when="@0.4:")
        depends_on("py-pyproj")
        depends_on("py-shapely")

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/o/odc-geo/{}-{}.tar.gz"
        if version >= Version("0.4.4"):
            name = "odc_geo"
        else:
            name = "odc-geo"
        return url.format(name, version)
