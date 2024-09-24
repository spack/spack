# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GlobusCommon(AutotoolsPackage):
    """Common aspects of the Grid Community Toolkit, based on a fork
    of the Globus Toolkit."""

    homepage = "https://github.com/gridcf/gct/tree/master/common/source"
    url = "https://repo.gridcf.org/gct6/sources/globus_common-18.14.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("18.14", sha256="22368942a78e608d8fe6d9f7379abc628e2bd7af54a98c7d2bddc265d6f0ba45")

    depends_on("c", type="build")
