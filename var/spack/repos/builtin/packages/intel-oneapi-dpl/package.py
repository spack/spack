# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import platform

from spack import *


class IntelOneapiDpl(IntelOneApiLibraryPackage):
    """Intel oneAPI DPL."""

    maintainers = ['rscohn2']

    homepage = 'https://github.com/oneapi-src/oneDPL'

    if platform.system() == 'Linux':
        version('2021.4.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17889/l_oneDPL_p_2021.4.0.337_offline.sh',
                sha256='540ef0d308c4b0f13ea10168a90edd42a56dc0883024f6f1a678b94c10b5c170',
                expand=False)

    @property
    def component_dir(self):
        return 'dpl'

    @property
    def headers(self):
        include_path = join_path(self.component_path, 'linux', 'include')
        headers = find_headers('*', include_path, recursive=True)
        # Force this directory to be added to include path, even
        # though no files are here because all includes are relative
        # to this path
        headers.directories = [include_path]
        return headers
