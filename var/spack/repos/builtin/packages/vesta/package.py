# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Vesta(Package):
    """VESTA is a 3D visualization program for structural models, volumetric data
       such as electron/nuclear densities, and crystal morphologies."""

    homepage = "http://jp-minerals.org/vesta"
    url      = "https://jp-minerals.org/vesta/archives/3.4.6/VESTA-x86_64.tar.bz2"

    version('3.4.6', '1d4651e86193f305831aa5db3dcfe789')

    depends_on('gtkplus@2.1.0:')
    depends_on('mesa')
    depends_on('cairo@1.0:')

    conflicts('%gcc@:5.3')

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', self.prefix)
        run_env.prepend_path('LD_LIBRARY_PATH', self.prefix)

    def install(self, spec, prefix):
        install_tree('.', prefix)
