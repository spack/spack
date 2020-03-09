# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class G4photonevaporation(Package):
    """Geant4 data for photon evaporation"""
    homepage = "http://geant4.web.cern.ch"
    url = "http://geant4-data.web.cern.ch/geant4-data/datasets/G4PhotonEvaporation.4.3.2.tar.gz"

    maintainers = ['drbenmorgan']

    version('4.3.2', sha256='d4641a6fe1c645ab2a7ecee09c34e5ea584fb10d63d2838248bfc487d34207c7')
    version('5.2', sha256='83607f8d36827b2a7fca19c9c336caffbebf61a359d0ef7cee44a8bcf3fc2d1f')

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, 'data'))
        install_path = join_path(prefix.share, 'data',
                                 'PhotonEvaporation{0}'
                                 .format(self.version))
        install_tree(self.stage.source_path, install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return ("http://geant4-data.web.cern.ch/geant4-data/datasets/G4PhotonEvaporation.%s.tar.gz" % version)
