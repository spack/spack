# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys
import os
from spack import *


class K8(Package):
    """K8 is a Javascript shell based on Google's V8 Javascript engine."""

    homepage = "https://github.com/attractivechaos/k8"
    url      = "https://github.com/attractivechaos/k8/releases/download/v0.2.4/k8-0.2.4.tar.bz2"

    version('0.2.4', 'edc5579ff18842a2a59aa92ce8bab8b4')

    depends_on('zlib', type='run')

    def install(self, spec, prefix):
        if (sys.platform == 'darwin'):
            os.rename('k8-Darwin', 'k8')

        if (sys.platform != 'darwin'):
            os.rename('k8-Linux', 'k8')
        install_tree('.', prefix.bin)
