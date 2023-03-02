# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


@IntelOneApiPackage.update_description
class IntelOneapiItac(IntelOneApiPackage):
    """The Intel Trace Analyzer and Collector profiles and analyzes MPI applications to help
    focus your optimization efforts.

    Find temporal dependencies and bottlenecks in your code.
    Check the correctness of your application.
    Locate potential programming errors, buffer overlaps, and deadlocks.
    Visualize and understand parallel application behavior.
    Evaluate profiling statistics and load balancing.
    Analyze performance of subroutines or code blocks.
    Learn about communication patterns, parameters, and performance data.
    Identify communication hot spots.
    Decrease time to solution and increase application efficiency.

    """

    homepage = "https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/trace-analyzer.html"

    maintainers("rscohn2")

    version(
        "2021.8.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/19129/l_itac_oneapi_p_2021.8.0.25341_offline.sh",
        sha256="9e943e07cbe7bcb2c6ec181cea5a2fd2241555bed695050f5069467fe7140c37",
        expand=False,
    )
    version(
        "2021.7.1",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/19024/l_itac_oneapi_p_2021.7.1.15324_offline.sh",
        sha256="fb26689efdb7369e211b5cf05f3e30d491a2787f24fef174b23241b997cc442f",
        expand=False,
    )
    version(
        "2021.7.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18886/l_itac_oneapi_p_2021.7.0.8707_offline.sh",
        sha256="719faeccfb1478f28110b72b1558187590a6f44cce067158f407ab335a7395bd",
        expand=False,
    )
    version(
        "2021.6.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18694/l_itac_oneapi_p_2021.6.0.434_offline.sh",
        sha256="1ecc2735da960041b051e377cadb9f6ab2f44e8aa44d0f642529a56a3cbba436",
        expand=False,
    )

    @property
    def component_dir(self):
        return "itac"
