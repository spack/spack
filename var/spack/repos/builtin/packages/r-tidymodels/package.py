# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
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
#     spack install r-tidymodels
#
# You can edit this file again by typing:
#
#     spack edit r-tidymodels
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class RTidymodels(RPackage):

    homepage = "https://cran.r-project.org/web/packages/tidymodels"
    url = "https://cran.r-project.org/web/packages/tidymodels/index.html/tidymodels_1.1.1.tar.gz"

    version("1.1.1", sha256="807e8e3cbdd81e495f6dc2ef14c9808780c4b992aa1b8b36ef9fa5b86aef95c6")

    depends_on("r-foo", type=("build", "run"))
