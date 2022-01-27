# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTidyverse(RPackage):
    """Easily Install and Load the 'Tidyverse'

    The 'tidyverse' is a set of packages that work in harmony because they
    share common data representations and 'API' design. This package is
    designed to make it easy to install and load multiple 'tidyverse' packages
    in a single step. Learn more about the 'tidyverse' at
    <https://tidyverse.org>."""

    homepage = "https://tidyverse.tidyverse.org/"
    cran = "tidyverse"

    version(
        "1.3.1",
        sha256="83cf95109d4606236274f5a8ec2693855bf75d3a1b3bc1ab4426dcc275ed6632",
    )
    version(
        "1.3.0",
        sha256="6d8acb81e994f9bef5e4dcf908bcea3786d108adcf982628235b6c8c80f6fe09",
    )
    version(
        "1.2.1",
        sha256="ad67a27bb4e89417a15338fe1a40251a7b5dedba60e9b72637963d3de574c37b",
    )

    depends_on("r@3.3:", when="@1.3.1:", type=("build", "run"))
    depends_on("r@3.2:", when="@1.3.0:", type=("build", "run"))
    depends_on("r+X", type=("build", "run"))

    depends_on("r-broom@0.7.6:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-broom@0.5.2:", when="@1.3.0:", type=("build", "run"))
    depends_on("r-broom@0.4.2:", type=("build", "run"))
    depends_on("r-cli@2.4.0:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-cli@1.1.0:", when="@1.3.0:", type=("build", "run"))
    depends_on("r-cli@1.0.0:", type=("build", "run"))
    depends_on("r-crayon@1.4.1:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-crayon@1.3.4:", type=("build", "run"))
    depends_on("r-dbplyr@2.1.1:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-dbplyr@1.4.2:", when="@1.3.0:", type=("build", "run"))
    depends_on("r-dbplyr@1.1.0:", type=("build", "run"))
    depends_on("r-dplyr@1.0.5:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-dplyr@0.8.3:", when="@1.3.0:", type=("build", "run"))
    depends_on("r-dplyr@0.7.4:", type=("build", "run"))
    depends_on("r-dtplyr@1.1.0:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-forcats@0.5.1:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-forcats@0.4.0:", when="@1.3.0:", type=("build", "run"))
    depends_on("r-forcats@0.2.0:", type=("build", "run"))
    depends_on("r-googledrive@1.0.1:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-googlesheets4@0.3.0:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-ggplot2@3.3.3:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-ggplot2@3.2.1:", when="@1.3.0:", type=("build", "run"))
    depends_on("r-ggplot2@2.2.1:", type=("build", "run"))
    depends_on("r-haven@2.3.1:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-haven@2.2.0:", when="@1.3.0:", type=("build", "run"))
    depends_on("r-haven@1.1.0:", type=("build", "run"))
    depends_on("r-hms@1.0.0:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-hms@0.5.2:", when="@1.3.0:", type=("build", "run"))
    depends_on("r-hms@0.3:", type=("build", "run"))
    depends_on("r-httr@1.4.2:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-httr@1.4.1:", when="@1.3.0:", type=("build", "run"))
    depends_on("r-httr@1.3.1:", type=("build", "run"))
    depends_on("r-jsonlite@1.7.2:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-jsonlite@1.6:", when="@1.3.0:", type=("build", "run"))
    depends_on("r-jsonlite@1.5:", type=("build", "run"))
    depends_on("r-lubridate@1.7.10:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-lubridate@1.7.4:", when="@1.3.0:", type=("build", "run"))
    depends_on("r-lubridate@1.7.1:", type=("build", "run"))
    depends_on("r-magrittr@2.0.1:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-magrittr@1.5:", type=("build", "run"))
    depends_on("r-modelr@0.1.8:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-modelr@0.1.5:", when="@1.3.0:", type=("build", "run"))
    depends_on("r-modelr@0.1.1:", type=("build", "run"))
    depends_on("r-pillar@1.6.0:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-pillar@1.4.2:", when="@1.3.0:", type=("build", "run"))
    depends_on("r-purrr@0.3.4:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-purrr@0.3.3:", when="@1.3.0:", type=("build", "run"))
    depends_on("r-purrr@0.2.4:", type=("build", "run"))
    depends_on("r-readr@1.4.0:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-readr@1.3.1:", when="@1.3.0:", type=("build", "run"))
    depends_on("r-readr@1.1.1:", type=("build", "run"))
    depends_on("r-readxl@1.3.1:", when="@1.3.0:", type=("build", "run"))
    depends_on("r-readxl@1.0.0:", type=("build", "run"))
    depends_on("r-reprex@2.0.0:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-reprex@0.3.0:", when="@1.3.0:", type=("build", "run"))
    depends_on("r-reprex@0.1.1:", type=("build", "run"))
    depends_on("r-rlang@0.4.10:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-rlang@0.4.1:", when="@1.3.0:", type=("build", "run"))
    depends_on("r-rlang@0.1.4:", type=("build", "run"))
    depends_on("r-rstudioapi@0.13:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-rstudioapi@0.10:", when="@1.3.0:", type=("build", "run"))
    depends_on("r-rstudioapi@0.7:", type=("build", "run"))
    depends_on("r-rvest@1.0.0:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-rvest@0.3.5:", when="@1.3.0:", type=("build", "run"))
    depends_on("r-rvest@0.3.2:", type=("build", "run"))
    depends_on("r-stringr@1.4.0:", when="@1.3.0:", type=("build", "run"))
    depends_on("r-stringr@1.2.0:", type=("build", "run"))
    depends_on("r-tibble@3.1.0:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-tibble@2.1.3:", when="@1.3.0:", type=("build", "run"))
    depends_on("r-tibble@1.3.4:", type=("build", "run"))
    depends_on("r-tidyr@1.1.3:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-tidyr@1.0.0:", when="@1.3.0:", type=("build", "run"))
    depends_on("r-tidyr@0.7.2:", type=("build", "run"))
    depends_on("r-xml2@1.3.2:", when="@1.3.1:", type=("build", "run"))
    depends_on("r-xml2@1.2.2:", when="@1.3.0:", type=("build", "run"))
    depends_on("r-xml2@1.1.1:", type=("build", "run"))
