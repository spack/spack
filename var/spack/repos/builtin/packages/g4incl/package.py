# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class G4incl(Package):
    """Geant4 data for evaluated particle cross-sections on natural
    composition of elements"""
    homepage = "https://geant4.web.cern.ch"
    url = "https://geant4-data.web.cern.ch/geant4-data/datasets/G4INCL.1.0.tar.gz"

    tags = ['hep']

    maintainers = ['drbenmorgan']

    # Only versions relevant to Geant4 releases built by spack are added
    version('1.0', sha256='716161821ae9f3d0565fbf3c2cf34f4e02e3e519eb419a82236eef22c2c4367d')

    # use geant4-config for version info
    executables = [r'^geant4-config$']

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, 'data'))
        install_path = join_path(prefix.share, 'data', "G4INCL{0}"
                                 .format(self.version))
        install_tree(self.stage.source_path, install_path)

    def setup_dependent_run_environment(self, env, dependent_spec):
        install_path = join_path(self.prefix.share, 'data', 'G4INCL{0}'
                                 .format(self.version))
        env.set('G4INCLDATA', install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return ("http://geant4-data.web.cern.ch/geant4-data/datasets/G4INCL.%s.tar.gz" % version)

    @classmethod
    def determine_spec_details(cls, prefix, exes_in_prefix):
        import os
        import re
        path = os.environ.get('G4INCLDATA', None)
        if not path:
            return
        pattern = '^(?P<prefix>.*?)/share/data/G4INCL(?P<version>.*?)$'
        match = re.match(pattern, path)
        prefix = match.group('prefix')
        version = match.group('version')
        s = Spec.from_detection('g4incl@' + version)
        s.external_path = prefix
        return s
