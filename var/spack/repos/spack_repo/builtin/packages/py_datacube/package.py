# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyDatacube(PythonPackage):
    """An analysis environment for satellite and other earth observation data."""

    homepage = "https://github.com/opendatacube/datacube-core"
    pypi = "datacube/datacube-1.8.3.tar.gz"

    license("Apache-2.0")
    maintainers("adamjstewart")

    version("1.9.3", sha256="f85fc33418874070710f11dae54d8e5570102973d5b12638142a51f5514f4360")
    version("1.8.3", sha256="d1e1a49c615fdaebf6e6008da7f925bc09e9d7bf94f259a1c596d266d1c36649")

    with default_args(type="build"):
        depends_on("py-setuptools@69:", when="@1.9:")
        depends_on("py-setuptools@42:")
        depends_on("py-setuptools-scm@3.4:+toml")

    with default_args(type=("build", "run")):
        depends_on("python@3.10:", when="@1.9:")
        depends_on("py-affine")
        depends_on("py-alembic", when="@1.9:")
        depends_on("py-antimeridian", when="@1.9:")
        depends_on("py-attrs@18.1:", when="@1.9:")
        depends_on("py-cachetools")
        depends_on("py-click@5:")
        depends_on("py-cloudpickle@0.4:")
        depends_on("py-dask+array")
        depends_on("py-deprecat", when="@1.9:")
        depends_on("py-distributed")
        depends_on("py-geoalchemy2", when="@1.9:")
        depends_on("py-jsonschema@4.18:", when="@1.9:")
        depends_on("py-jsonschema")
        depends_on("py-lark", when="@1.9:")
        depends_on("py-lark@0.6.7:", when="@:1.8")
        depends_on("py-numpy@1.26:", when="@1.9:")
        depends_on("py-numpy")
        depends_on("py-odc-geo@0.4.8:", when="@1.9:")
        depends_on("py-packaging", when="@1.9:")
        depends_on("py-pandas", when="@1.9:")
        depends_on("py-pyproj@2.5:")
        depends_on("py-python-dateutil")
        depends_on("py-pyyaml")
        depends_on("py-rasterio@1.3.11:", when="@1.9:")
        depends_on("py-rasterio@1.0.2:")
        depends_on("py-ruamel-yaml", when="@1.9:")
        depends_on("py-shapely@2:", when="@1.9:")
        depends_on("py-shapely@1.6.4:")
        depends_on("py-sqlalchemy@2:", when="@1.9:")
        depends_on("py-sqlalchemy")
        depends_on("py-toolz")
        depends_on("py-xarray@0.9:")

        # Historical dependencies
        depends_on("py-netcdf4", when="@:1.8")
        depends_on("py-psycopg2", when="@:1.8")
