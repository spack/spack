# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Lsf(Package):
    """IBM Platform LSF is a batch scheduler for HPC environments"""

    homepage = "https://www.ibm.com/marketplace/hpc-workload-management"

    # LSF needs to be added as an external package to SPACK. For this, the
    # config file packages.yaml needs to be adjusted:
    #   lsf:
    #     version: [10.1]
    #     paths:
    #       lsf@10.1: /usr/local/lsf/10.1 (path to your LSF installation)
    #     buildable: False

    def install(self, spec, prefix):
        raise InstallError('LSF is not installable; it is vendor supplied')
