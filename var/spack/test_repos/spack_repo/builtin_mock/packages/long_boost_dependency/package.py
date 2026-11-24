# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class LongBoostDependency(Package):
    """Simple package with one optional dependency"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version("1.0")

    variant("longdep", description="enable boost dependency", default=True)

    depends_on("boost+atomic+chrono+date_time+filesystem+graph+iostreams+locale", when="+longdep")
    depends_on("boost", when="~longdep")
