# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTidymodels(RPackage):

    homepage = "https://cran.r-project.org/web/packages/tidymodels"
    url = "https://cran.r-project.org/web/packages/tidymodels/index.html/tidymodels_1.1.1.tar.gz"

    version("1.1.1", sha256="807e8e3cbdd81e495f6dc2ef14c9808780c4b992aa1b8b36ef9fa5b86aef95c6")

    depends_on("r-foo", type=("build", "run"))
