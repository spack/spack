# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Jmol(Package):
    """Jmol: an open-source Java viewer for chemical structures in 3D
    with features for chemicals, crystals, materials and biomolecules."""

    homepage = "http://jmol.sourceforge.net/"
    url      = "https://sourceforge.net/projects/jmol/files/Jmol/Version%2014.8/Jmol%2014.8.0/Jmol-14.8.0-binary.tar.gz"

    version('14.8.0', '3c9f4004b9e617ea3ea0b78ab32397ea')

    depends_on('java', type='run')

    def install(self, spec, prefix):
        install_tree('jmol-{0}'.format(self.version), prefix)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', self.prefix)
        run_env.set('JMOL_HOME', self.prefix)
