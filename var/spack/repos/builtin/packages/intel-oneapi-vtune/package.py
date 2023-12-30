# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


@IntelOneApiPackage.update_description
class IntelOneapiVtune(IntelOneApiLibraryPackageWithSdk):
    """Intel VTune Profiler is a profiler to optimize application
    performance, system performance, and system configuration for HPC,
    cloud, IoT, media, storage, and more.  CPU, GPU, and FPGA: Tune
    the entire application's performance--not just the accelerated
    portion. Multilingual: Profile SYCL, C, C++, C#, Fortran, OpenCL
    code, Python, Google Go programming language, Java, .NET,
    Assembly, or any combination of languages.  System or Application:
    Get coarse-grained system data for an extended period or detailed
    results mapped to source code. Power: Optimize performance while
    avoiding power and thermal-related throttling.

    """

    maintainers("rscohn2")

    homepage = "https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/vtune-profiler.html"

    version(
        "2024.0.0",
        url="https://registrationcenter-download.intel.com/akdlm//IRC_NAS/1722cc83-ceb2-4304-b4dc-2813780222a3/l_oneapi_vtune_p_2024.0.0.49503_offline.sh",
        sha256="09537329bdf6e105b0e164f75dc8ae122adc99a64441f6a52225509bcff3b848",
        expand=False,
    )
    version(
        "2023.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/dfae6f23-6c90-4b9f-80e2-fa2a5037fe36/l_oneapi_vtune_p_2023.2.0.49485_offline.sh",
        sha256="482a727afe0ac6f81eff51503857c28fcb79ffdba76260399900f3397fd0adbd",
        expand=False,
    )
    version(
        "2023.1.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/4466ed1b-5d4a-4b30-9146-1eabc336c647/l_oneapi_vtune_p_2023.1.0.44286_offline.sh",
        sha256="4730552281d03e40370be300044e724c65e596f5062fddb002ed7b52de630a75",
        expand=False,
    )
    version(
        "2023.0.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/19136/l_oneapi_vtune_p_2023.0.0.25339_offline.sh",
        sha256="77fb356b501177d7bd5c936729ba4c1ada45935dc45a8ecd2f1164c276feb1ea",
        expand=False,
    )
    version(
        "2022.4.1",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/19027/l_oneapi_vtune_p_2022.4.1.16919_offline.sh",
        sha256="eb4b4da61eea52c08fc139dbf4630e2c52cbcfaea8f1376c545c0863839366d1",
        expand=False,
    )
    version(
        "2022.4.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18888/l_oneapi_vtune_p_2022.4.0.8705_offline.sh",
        sha256="8c5a144ed61ef9addaa41abe7fbfceeedb6a8fe1c5392e3e265aada1f545b0fe",
        expand=False,
    )
    version(
        "2022.3.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18656/l_oneapi_vtune_p_2022.3.0.195_offline.sh",
        sha256="7921fce7fcc3b82575be22d9c36beec961ba2a9fb5262ba16a04090bcbd2e1a6",
        expand=False,
    )
    version(
        "2022.0.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18406/l_oneapi_vtune_p_2022.0.0.94_offline.sh",
        sha256="aa4d575c22e7be0c950b87d67d9e371f470f682906864c4f9b68e530ecd22bd7",
        expand=False,
    )
    version(
        "2021.7.1",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18086/l_oneapi_vtune_p_2021.7.1.492_offline.sh",
        sha256="4cf17078ae6e09f26f70bd9d0b726af234cc30c342ae4a8fda69941b40139b26",
        expand=False,
    )
    version(
        "2021.6.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18012/l_oneapi_vtune_p_2021.6.0.411_offline.sh",
        sha256="6b1df7da713337aa665bcc6ff23e4a006695b5bfaf71dffd305cbadca2e5560c",
        expand=False,
    )

    @property
    def v2_layout_versions(self):
        return "@2024:"

    @property
    def component_dir(self):
        return "vtune"
