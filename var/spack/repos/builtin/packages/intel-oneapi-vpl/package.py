# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack import *


class IntelOneapiVpl(IntelOneApiLibraryPackage):
    """Intel oneAPI VPL."""

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/onevpl.html'

    if platform.system() == 'Linux':
        version('2021.6.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18190/l_oneVPL_p_2021.6.0.458_offline.sh',
                sha256='40c50008be3f03d17cc8c0c34324593c1d419ee4c45af5543aa5a2d5fb11071f',
                expand=False)
        version('2021.2.2',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17733/l_oneVPL_p_2021.2.2.212_offline.sh',
                sha256='21106ba5cde22f3e31fd55280fbccf263508fa054030f12d5dff4a5379ef3bb7',
                expand=False)
        version('2021.1.1',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17418/l_oneVPL_p_2021.1.1.66_offline.sh',
                sha256='0fec42545b30b7bb2e4e33deb12ab27a02900f5703153d9601673a8ce43082ed',
                expand=False)

    @property
    def component_dir(self):
        return 'vpl'
