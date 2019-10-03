# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class G4ensdfstate(Package):
    """Geant4 data for nuclides properties"""
    homepage = "http://geant4.web.cern.ch"
    url = "http://geant4-data.web.cern.ch/geant4-data/datasets/G4ENSDFSTATE.2.1.tar.gz"

    version('2.1', '933e7f99b1c70f24694d12d517dfca36d82f4e95b084c15d86756ace2a2790d9')
    version('2.2', 'dd7e27ef62070734a4a709601f5b3bada6641b111eb7069344e4f99a01d6e0a6')

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, 'data'))
        install_path = join_path(prefix.share, 'data', 'G4ENSDFSTATE{0}'
                                 .format(self.version))
        install_tree(self.stage.source_path, install_path)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        run_env.set('G4ENSDFSTATEDATA', join_path(prefix.share, 'data'))

    def url_for_version(self, version):
        """Handle version string."""
        return "http://geant4-data.web.cern.ch/geant4-data/datasets/G4ENSDFSTATE.%s.tar.gz" % version
