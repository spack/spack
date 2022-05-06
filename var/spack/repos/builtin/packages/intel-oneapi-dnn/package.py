# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import platform

from spack import *


class IntelOneapiDnn(IntelOneApiLibraryPackage):
    __doc__ = ("""Intel oneAPI DNN."""
               + IntelOneApiPackage.license_text)

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/onednn.html'

    if platform.system() == 'Linux':
        version('2022.1.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18725/l_onednn_p_2022.1.0.132_offline.sh',
                sha256='0b9a7efe8dd0f0b5132b353a8ee99226f75bae4bab188a453817263a0684cc93',
                expand=False)
        version('2022.0.2',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18476/l_onednn_p_2022.0.2.43_offline.sh',
                sha256='a2a953542b4f632b51a2527d84bd76c3140a41c8085420da4237e2877c27c280',
                expand=False)
        version('2022.0.1',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18441/l_onednn_p_2022.0.1.26_offline.sh',
                sha256='8339806300d83d2629952e6e2f2758b52f517c072a20b7b7fc5642cf1e2a5410',
                expand=False)
        version('2021.4.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18221/l_onednn_p_2021.4.0.467_offline.sh',
                sha256='30cc601467f6a94b3d7e14f4639faf0b12fdf6d98df148b07acdb4dfdfb971db',
                expand=False)
        version('2021.3.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17923/l_onednn_p_2021.3.0.344_offline.sh',
                sha256='1521f6cbffcf9ce0c7b5dfcf1a2546a4a0c8d8abc99f3011709039aaa9e0859a',
                expand=False)
        version('2021.2.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17751/l_onednn_p_2021.2.0.228_offline.sh',
                sha256='62121a3355298211a124ff4e71c42fc172bf1061019be6c6120830a1a502aa88',
                expand=False)
        version('2021.1.1',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17385/l_onednn_p_2021.1.1.55_offline.sh',
                sha256='24002c57bb8931a74057a471a5859d275516c331fd8420bee4cae90989e77dc3',
                expand=False)

    depends_on('intel-oneapi-tbb')

    @property
    def component_dir(self):
        return 'dnnl'

    @property
    def headers(self):
        include_path = join_path(self.component_path, 'cpu_dpcpp_gpu_dpcpp', 'include')
        return find_headers('dnnl', include_path)

    @property
    def libs(self):
        lib_path = join_path(self.component_path, 'cpu_dpcpp_gpu_dpcpp', 'lib')
        return find_libraries(['libdnnl', 'libmkldnn'], root=lib_path, shared=True)
