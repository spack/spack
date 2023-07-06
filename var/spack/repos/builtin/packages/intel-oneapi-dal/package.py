# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


@IntelOneApiPackage.update_description
class IntelOneapiDal(IntelOneApiLibraryPackage):
    """Intel oneAPI Data Analytics Library (oneDAL) is a library that
    helps speed up big data analysis by providing highly optimized
    algorithmic building blocks for all stages of data analytics
    (preprocessing, transformation, analysis, modeling, validation,
    and decision making) in batch, online, and distributed
    processing modes of computation. The library optimizes data
    ingestion along with algorithmic computation to increase
    throughput and scalability.

    """

    maintainers("rscohn2")

    homepage = (
        "https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/onedal.html"
    )

    version(
        "2023.1.0",
        url="https://registrationcenter-download.intel.com/akdlm/IRC_NAS/c209d29f-3d06-45fb-8f04-7b2f47b93a7c/l_daal_oneapi_p_2023.1.0.46349_offline.sh",
        sha256="5ed5c021a2d3c0e65702d0ae3e18010a85af18bdfbc534e783797d3b23c56801",
        expand=False,
    )
    version(
        "2023.0.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/19122/l_daal_oneapi_p_2023.0.0.25395_offline.sh",
        sha256="83d0ca7501c882bf7e1f250e7310dafa6b6fd404858298ce9cde7546654d43bc",
        expand=False,
    )
    version(
        "2021.7.1",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/19032/l_daal_oneapi_p_2021.7.1.16996_offline.sh",
        sha256="2328927480b0ba5d380028f981717b63ee323f8a1616a491a160a0a0b239e285",
        expand=False,
    )
    version(
        "2021.7.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18895/l_daal_oneapi_p_2021.7.0.8746_offline.sh",
        sha256="c18e68df120c2b1db17877cfcbb1b5c93a47b2f4756a3444c663d0f03be4eee3",
        expand=False,
    )
    version(
        "2021.6.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18698/l_daal_oneapi_p_2021.6.0.915_offline.sh",
        sha256="bc9a430f372a5f9603c19ec25207c83ffd9d59fe517599c734d465e32afc9790",
        expand=False,
    )
    version(
        "2021.5.3",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18480/l_daal_oneapi_p_2021.5.3.832_offline.sh",
        sha256="6d3503cf7be2908bbb7bd18e67b8f2e96ad9aec53d4813c9be620adaa2db390f",
        expand=False,
    )
    version(
        "2021.5.1",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18432/l_daal_oneapi_p_2021.5.1.803_offline.sh",
        sha256="bba7bee3caef14fbb54ad40615222e5da429496455edf7375f11fd84a72c87ba",
        expand=False,
    )
    version(
        "2021.4.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/18218/l_daal_oneapi_p_2021.4.0.729_offline.sh",
        sha256="61da9d2a40c75edadff65d052fd84ef3db1da5d94f86ad3956979e6988549dda",
        expand=False,
    )
    version(
        "2021.3.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/17905/l_daal_oneapi_p_2021.3.0.557_offline.sh",
        sha256="4c2e77a3a2fa5f8a09b7d68760dfca6c07f3949010836cd6da34075463467995",
        expand=False,
    )
    version(
        "2021.2.0",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/17747/l_daal_oneapi_p_2021.2.0.358_offline.sh",
        sha256="cbf4e64dbd21c10179f2d1d7e8b8b0f12eeffe6921602df33276cd0ebd1f8e34",
        expand=False,
    )
    version(
        "2021.1.1",
        url="https://registrationcenter-download.intel.com/akdlm/irc_nas/17443/l_daal_oneapi_p_2021.1.1.79_offline.sh",
        sha256="6e0e24bba462e80f0fba5a46e95cf0cca6cf17948a7753f8e396ddedd637544e",
        expand=False,
    )

    depends_on("tbb")

    provides("daal")
    provides("onedal")

    @property
    def component_dir(self):
        return "dal"
