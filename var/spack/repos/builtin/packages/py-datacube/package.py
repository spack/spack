# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDatacube(PythonPackage):
    """An analysis environment for satellite and other earth observation data."""

    homepage = "https://github.com/opendatacube/datacube-core"
    pypi = "datacube/datacube-1.8.3.tar.gz"

    maintainers("adamjstewart")

    license("Apache-2.0")

    version(
        "1.8.3",
        sha256="2685684ba57bd05f5438d3cc54f8a4c7e6b246933d11c66cff255680cf1d73b6",
        url="https://pypi.org/packages/24/6b/007cd4e702d895114151407534d654c70cac8d9e274b70dd854b7b4c56d7/datacube-1.8.3-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-affine")
        depends_on("py-cachetools")
        depends_on("py-click@5:")
        depends_on("py-cloudpickle@0.4:")
        depends_on("py-dask+array")
        depends_on("py-distributed", when="@1.8:")
        depends_on("py-jsonschema", when="@:1.8.15")
        depends_on("py-lark-parser@0.6.7:", when="@1.7-rc1:1.8.7")
        depends_on("py-netcdf4", when="@:1.8,1.9.0-rc2")
        depends_on("py-numpy")
        depends_on("py-psycopg2")
        depends_on("py-pyproj@2.5:", when="@1.8:")
        depends_on("py-python-dateutil")
        depends_on("py-pyyaml")
        depends_on("py-rasterio@1.0.2:", when="@:1.8.7")
        depends_on("py-shapely@1.6.4:", when="@1.8:1.8.9")
        depends_on("py-sqlalchemy", when="@:1.8.9")
        depends_on("py-toolz")
        depends_on("py-xarray@0.9.0:", when="@:1.8.7,1.8.10:")

    # Excluding 'datacube.utils.aws' since it requires 'boto3'
    import_modules = [
        "datacube_apps",
        "datacube_apps.stacker",
        "datacube",
        "datacube.ui",
        "datacube.drivers",
        "datacube.drivers.rio",
        "datacube.drivers.postgres",
        "datacube.drivers.netcdf",
        "datacube.utils",
        "datacube.utils.rio",
        "datacube.utils.geometry",
        "datacube.storage",
        "datacube.execution",
        "datacube.virtual",
        "datacube.scripts",
        "datacube.model",
        "datacube.api",
        "datacube.index",
        "datacube.testutils",
    ]
