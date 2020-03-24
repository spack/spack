# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Jmol(Package):
    """Jmol: an open-source Java viewer for chemical structures in 3D
    with features for chemicals, crystals, materials and biomolecules."""

    homepage = "http://jmol.sourceforge.net/"
    url      = "https://sourceforge.net/projects/jmol/files/Jmol/Version%2014.8/Jmol%2014.8.0/Jmol-14.8.0-binary.tar.gz"

    version('14.8.0', sha256='8ec45e8d289aa0762194ca71848edc7d736121ddc72276031a253a3651e6d588')

    depends_on('java', type='run')

    def install(self, spec, prefix):
        install_tree('jmol-{0}'.format(self.version), prefix)

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self.prefix)
        env.set('JMOL_HOME', self.prefix)
