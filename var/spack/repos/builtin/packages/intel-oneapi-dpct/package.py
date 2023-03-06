# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


@IntelOneApiPackage.update_description
class IntelOneapiDpct(IntelOneApiPackage):
    """The Intel DPC++ Compatibility Tool assists in migrating your
    existing CUDA code to SYCL code. The tool ports both CUDA
    language kernels and library API calls. Typically, 90%-95% of
    CUDA code automatically migrates to SYCL code.

    """

    maintainers("rscohn2")

    homepage = "https://www.intel.com/content/www/us/en/developer/tools/oneapi/dpc-compatibility-tool.html#gs.2p8km6"

    version(
        "2023.0.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/19100/l_dpcpp-ct_p_2023.0.0.25483_offline.sh",
        sha256="81f392d16a10cbdb8e9d053f18566304a78e1be624280ad43ddbc0dfd767fc7f",
        expand=False,
    )
    version(
        "2022.2.1",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18991/l_dpcpp-ct_p_2022.2.1.14994_offline.sh",
        sha256="ea2fbe36de70eb3c78c97133f81e0b2a2fbcfc9525e77125a183d7af446ef3e6",
        expand=False,
    )
    version(
        "2022.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18908/l_dpcpp-ct_p_2022.2.0.8701_offline.sh",
        sha256="ca79b89ba4b97accb868578a1b7ba0e38dc5e4457d45c6c2552ba33d71b52128",
        expand=False,
    )
    version(
        "2022.1.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18746/l_dpcpp-ct_p_2022.1.0.172_offline.sh",
        sha256="ec42f4df3f9daf1af587b14b8b6644c773a0b270e03dd22ac9e2f49131e3e40c",
        expand=False,
    )

    @property
    def component_dir(self):
        return "dpcpp-ct"
