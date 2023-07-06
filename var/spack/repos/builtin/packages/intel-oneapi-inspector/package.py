# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


@IntelOneApiPackage.update_description
class IntelOneapiInspector(IntelOneApiPackage):
    """Intel Inspector is a dynamic memory and threading error debugger
    for C, C++, and Fortran applications that run on Windows and Linux
    operating systems.  Save money: locate the root cause of memory,
    threading, and persistence errors before you release.  Save time:
    simplify the diagnosis of difficult errors by breaking into the
    debugger just before the error occurs.  Save effort: use your
    normal debug or production build to catch and debug errors. Check
    all code, including third-party libraries with unavailable
    sources.

    """

    maintainers("rscohn2")

    homepage = "https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/inspector.html"

    version(
        "2023.1.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/5e922b71-d701-4a88-b447-eb88fcb630e2/l_inspector_oneapi_p_2023.1.0.43486_offline.sh",
        sha256="e41b31978c445faeccc1b3820a987746f922bae0bbfcf6cbafe082beede4e712",
        expand=False,
    )
    version(
        "2023.0.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/19125/l_inspector_oneapi_p_2023.0.0.25340_offline.sh",
        sha256="adae2f06443c62a1a7be6aff2ad9c78672ec70f67b83dd660e68faafd7911dd4",
        expand=False,
    )
    version(
        "2022.3.1",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/19005/l_inspector_oneapi_p_2022.3.1.15318_offline.sh",
        sha256="62aa2abf6928c0f4fc60ccfb69375297f823c183aea2519d7344e09c9734c1f8",
        expand=False,
    )
    version(
        "2022.3.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18924/l_inspector_oneapi_p_2022.3.0.8706_offline.sh",
        sha256="c239b93769afae0ef5f7d3b8584d739bf4a839051bd428f1e6be3e8ca5d4aefa",
        expand=False,
    )
    version(
        "2022.1.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18712/l_inspector_oneapi_p_2022.1.0.123_offline.sh",
        sha256="8551180aa30be3abea11308fb11ea9a296f0e056ab07d9254585448a0b23333e",
        expand=False,
    )
    version(
        "2022.0.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18363/l_inspector_oneapi_p_2022.0.0.56_offline.sh",
        sha256="79a0eb2ae3f1de1e3456076685680c468702922469c3fda3e074718fb0bea741",
        expand=False,
    )
    version(
        "2021.4.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18239/l_inspector_oneapi_p_2021.4.0.266_offline.sh",
        sha256="c8210cbcd0e07cc75e773249a5e4a02cf34894ec80a213939f3a20e6c5705274",
        expand=False,
    )
    version(
        "2021.3.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/17946/l_inspector_oneapi_p_2021.3.0.217_offline.sh",
        sha256="1371ca74be2a6d4b069cdb3f8f2d6109abbc3261a81f437f0fe5412a7b659b43",
        expand=False,
    )

    @property
    def component_dir(self):
        return "inspector"
