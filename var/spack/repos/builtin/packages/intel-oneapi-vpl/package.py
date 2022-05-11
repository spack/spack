# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.util.package import *


@IntelOneApiPackage.update_description
class IntelOneapiVpl(IntelOneApiLibraryPackage):
    """The Intel oneAPI Video Processing Library (oneVPL) is the successor
    to Intel Media SDK. This library takes you from abstractions for
    integrated graphics to using oneVPL to unlock media features on a
    much broader range of accelerators.  oneVPL provides a single,
    video-focused API for encoding, decoding, and video processing
    that works across a wide range of accelerators. The library is
    perfect for applications spanning broadcasting, streaming, video
    on demand (VOD), in-cloud gaming, and remote desktop solutions.

    """

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/onevpl.html'

    if platform.system() == 'Linux':
        version('2022.1.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18750/l_oneVPL_p_2022.1.0.154_offline.sh',
                sha256='486cca918c9772a43f62da77e07cdf54dabb92ecebf494eb8c89c4492ab43447',
                expand=False)
        version('2022.0.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18375/l_oneVPL_p_2022.0.0.58_offline.sh',
                sha256='600b8566e1aa523b97291bed6b08f69a04bc7c4c75c035942a64a38f45a1a7f0',
                expand=False)
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
