# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class G4neutronxs(Package):
    """Geant4 data for evaluated neutron cross-sections on natural composition
       of elements"""
    homepage = "https://geant4.web.cern.ch"
    url = "https://geant4-data.web.cern.ch/geant4-data/datasets/G4NEUTRONXS.1.4.tar.gz"

    tags = ['hep']

    maintainers = ['drbenmorgan']

    # Only versions relevant to Geant4 releases built by spack are added
    # Dataset not used after Geant4 10.4.x
    version('1.4', sha256='57b38868d7eb060ddd65b26283402d4f161db76ed2169437c266105cca73a8fd')

    # use geant4-config for version info
    executables = [r'^geant4-config$']

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, 'data'))
        install_path = join_path(prefix.share, 'data', 'G4NEUTRONXS{0}'
                                 .format(self.version))
        install_tree(self.stage.source_path, install_path)

    def setup_dependent_run_environment(self, env, dependent_spec):
        install_path = join_path(self.prefix.share, 'data', 'G4NEUTRONXS{0}'
                                 .format(self.version))
        env.set('G4NEUTRONXSDATA', install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return "http://geant4-data.web.cern.ch/geant4-data/datasets/G4NEUTRONXS.%s.tar.gz" % version

    @classmethod
    def determine_spec_details(cls, prefix, exes_in_prefix):
        import os
        import re
        path = os.environ.get('G4NEUTRONXSDATA', None)
        if not path:
            return
        match = re.match('^(?P<prefix>.*?)/share/data/G4NEUTRONXS(?P<version>.*?)$', path)
        prefix = match.group('prefix')
        version = match.group('version')
        s = Spec.from_detection('g4neutronxs@' + version)
        s.external_path = prefix
        return s
