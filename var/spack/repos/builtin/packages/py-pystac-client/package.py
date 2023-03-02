# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPystacClient(PythonPackage):
    """Python library for working with Spatiotemporal Asset Catalog (STAC)."""

    homepage = "https://github.com/stac-utils/pystac-client.git"
    pypi = "pystac-client/pystac-client-0.5.1.tar.gz"

    version("0.5.1", sha256="f585bd9bcd52ee399c8a292dbb7e0405c0da359a73bc07c1ef82a65c17124d94")

    depends_on("py-setuptools", type="build")
    depends_on("py-requests@2.27.1:", type=("build", "run"))
    depends_on("py-pystac@1.4:", type=("build", "run"))
    depends_on("py-python-dateutil@2.7:", type=("build", "run"))
