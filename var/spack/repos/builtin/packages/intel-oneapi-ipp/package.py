# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


@IntelOneApiPackage.update_description
class IntelOneapiIpp(IntelOneApiLibraryPackage):
    """Intel Integrated Performance Primitives (Intel IPP) is an extensive
    library of ready-to-use, domain-specific functions that are
    highly optimized for diverse Intel architectures. These
    functions take advantage of Single Instruction, Multiple Data
    (SIMD) instructions and improve the performance of
    computation-intensive applications, including signal
    processing, data compression, video processing, and
    cryptography. The intel-oneapi-ippcp package contains support
    for cryptography and everything else can be found in the
    intel-oneapi-ipp package.

    """

    maintainers("rscohn2")

    homepage = (
        "https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/ipp.html"
    )

    version(
        "2021.8.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/732392fa-41b3-4a92-935e-6a2b823162a7/l_ipp_oneapi_p_2021.8.0.46345_offline.sh",
        sha256="d3348f37d03583dc767d3e3e8b5f0208405772de7991bd9d52112d83d332b749",
        expand=False,
    )
    version(
        "2021.7.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/19126/l_ipp_oneapi_p_2021.7.0.25396_offline.sh",
        sha256="98b40cb6cea2198480400579330a5de85fd58d441b323246dfd2b960990fec26",
        expand=False,
    )
    version(
        "2021.6.2",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/19007/l_ipp_oneapi_p_2021.6.2.16995_offline.sh",
        sha256="23ae49afa9f13c2bed0c8a32e447e1c6b3528685cebdd32e4aa2a9736827cc4e",
        expand=False,
    )
    version(
        "2021.6.1",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18925/l_ipp_oneapi_p_2021.6.1.8749_offline.sh",
        sha256="3f8705bf57c07b71d822295bfad49b531a38b6c3a4ca1119e4c52236cb664f57",
        expand=False,
    )
    version(
        "2021.6.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18748/l_ipp_oneapi_p_2021.6.0.626_offline.sh",
        sha256="cf09b5229dd38d75671fa1ab1af47e4d5f9f16dc7c9c22a4313a221a184774aa",
        expand=False,
    )
    version(
        "2021.5.2",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18474/l_ipp_oneapi_p_2021.5.2.544_offline.sh",
        sha256="ba48d91ab1447d0ae3d3a5448e3f08e460393258b60630c743be88281e51608e",
        expand=False,
    )
    version(
        "2021.5.1",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18440/l_ipp_oneapi_p_2021.5.1.522_offline.sh",
        sha256="be99f9b0b2cc815e017188681ab997f3ace94e3010738fa6f702f2416dac0de4",
        expand=False,
    )
    version(
        "2021.4.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18219/l_ipp_oneapi_p_2021.4.0.459_offline.sh",
        sha256="1a7a8fe5502ae61c10f5c432b7662c6fa542e5832a40494eb1c3a2d8e27c9f3e",
        expand=False,
    )
    version(
        "2021.3.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/17958/l_ipp_oneapi_p_2021.3.0.333_offline.sh",
        sha256="67e75c80813ec9a30d5fda5860f76122ae66fa2128a48c8461f5e6b100b38bbb",
        expand=False,
    )
    version(
        "2021.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/17758/l_ipp_oneapi_p_2021.2.0.233_offline.sh",
        sha256="ccdfc81f77203822d80151b40ce9e8fd82bb2de85a9b132ceed12d24d3f3ff52",
        expand=False,
    )
    version(
        "2021.1.1",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/17436/l_ipp_oneapi_p_2021.1.1.47_offline.sh",
        sha256="2656a3a7f1f9f1438cbdf98fd472a213c452754ef9476dd65190a7d46618ba86",
        expand=False,
    )

    depends_on("tbb")

    provides("ipp")

    @property
    def component_dir(self):
        return "ipp"
