# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


@IntelOneApiPackage.update_description
class IntelOneapiCompilersClassic(Package):
    """Relies on intel-oneapi-compilers to install the compilers, and
    configures modules for icc/icpc/ifort.

    """

    maintainers = ['rscohn2']

    homepage = "https://software.intel.com/content/www/us/en/develop/tools/oneapi.html"

    has_code = False

    phases = []

    for ver in ['2022.1.0',
                '2022.0.2',
                '2022.0.1',
                '2021.4.0',
                '2021.3.0',
                '2021.2.0',
                '2021.1.2']:
        version(ver)
        depends_on('intel-oneapi-compilers@' + ver, when='@' + ver)

    def setup_run_environment(self, env):
        """Adds environment variables to the generated module file.

        These environment variables come from running:

        .. code-block:: console

           $ source {prefix}/{component}/{version}/env/vars.sh

        and from setting CC/CXX/F77/FC
        """
        bin = join_path(self.spec['intel-oneapi-compilers'].prefix,
                        'compile', 'linux', 'bin', 'intel64')
        env.set('CC', join_path(bin, 'icc'))
        env.set('CXX', join_path(bin, 'icpc'))
        env.set('F77', join_path(bin, 'ifort'))
        env.set('FC', join_path(bin, 'ifort'))
