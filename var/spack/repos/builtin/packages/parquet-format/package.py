# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ParquetFormat(MavenPackage):
    """ParquetFormat is a columnar storage format that supports nested data."""

    homepage = "https://github.com/apache/parquet-format/"
    url = "https://github.com/apache/parquet-format/archive/apache-parquet-format-2.8.0.tar.gz"

    license("Apache-2.0")

    version("2.11.0", sha256="ed7f5a91db0567a221bc5b61624589b8b7f816588ee4b15a34d7a99b9bec7e7c")
    version("2.8.0", sha256="345c044cea73997162e0c38ae830509ee424faf49c90974e4f244079a3df01b0")
    version("2.7.0", sha256="e821ffc67f61b49afce017ce2d1d402b4df352ca49dbeae167b06c4d3264b6ba")

    # pom.xml
    depends_on("thrift@0.21.0", when="@2.11")
    depends_on("thrift@0.12.0", when="@2.7:2.8")
    depends_on("java@8", type=("build", "run"))
