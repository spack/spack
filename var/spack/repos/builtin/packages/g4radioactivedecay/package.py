# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class G4radioactivedecay(Package):
    """Geant4 data files for radio-active decay hadronic processes"""
    homepage = "http://geant4.web.cern.ch"
    url = "http://geant4-data.web.cern.ch/geant4-data/datasets/G4RadioactiveDecay.5.1.1.tar.gz"

    version('5.1.1', 'f7a9a0cc998f0d946359f2cb18d30dff1eabb7f3c578891111fc3641833870ae')
    version('5.2', '99c038d89d70281316be15c3c98a66c5d0ca01ef575127b6a094063003e2af5d')

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, 'data'))
        install_path = join_path(prefix.share, 'data', 'RadioactiveDecay{0}'
                                 .format(self.version))
        install_tree(self.stage.source_path, install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return ("http://geant4-data.web.cern.ch/geant4-data/datasets/G4RadioactiveDecay.%s.tar.gz" % version)
