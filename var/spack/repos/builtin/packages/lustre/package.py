# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lustre(Package):
    """Lustre is a type of parallel distributed file system,
       generally used for large-scale cluster computing."""

    homepage = 'http://lustre.org/'
    has_code = False

    version('2.12')

    # Lustre is filesystem and needs to be installed on system.
    # To have it as external package in SPACK, follow below:
    # config file packages.yaml needs to be adjusted:
    #   lustre:
    #     version: [2.12]
    #     paths:
    #       lustre@2.12: /usr (Usual Lustre library path)
    #     buildable: False

    def install(self, spec, prefix):
        raise InstallError(
            self.spec.format('{name} is not installable, you need to specify '
                             'it as an external package in packages.yaml'))
