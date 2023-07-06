# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RForeign(RPackage):
    """Read Data Stored by 'Minitab', 'S', 'SAS', 'SPSS', 'Stata', 'Systat',
    'Weka', 'dBase', ...

    Reading and writing data stored by some versions of 'Epi Info', 'Minitab',
    'S', 'SAS', 'SPSS', 'Stata', 'Systat', 'Weka', and for reading and writing
    some 'dBase' files."""

    cran = "foreign"

    version("0.8-84", sha256="17edf302c7568a122dc496a61a4a886ef7c02224a235d945b473611c79c98549")
    version("0.8-83", sha256="87eae73f780b6bbcf0a45b3e21d1c87be0404aa2d5b455df92ab45516030721b")
    version("0.8-82", sha256="f8ed0684d59bec7f3a39cde1aa5ec7b3e6e36aaecacb28120c9c54f7b13f80fb")
    version("0.8-81", sha256="1ae8f9f18f2a037697fa1a9060417ff255c71764f0145080b2bd23ba8262992c")
    version("0.8-72", sha256="439c17c9cd387e180b1bb640efff3ed1696b1016d0f7b3b3b884e89884488c88")
    version("0.8-70.2", sha256="ae82fad68159860b8ca75b49538406ef3d2522818e649d7ccc209c18085ef179")
    version("0.8-66", sha256="d7401e5fcab9ce6e697d3520dbb8475e229c30341c0004c4fa489c82aa4447a4")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@4.0.0:", type=("build", "run"), when="@0.8-81:")
