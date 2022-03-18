# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class G4pii(Package):
    """Geant4 data for shell ionisation cross-sections"""
    homepage = "https://geant4.web.cern.ch"
    url = "https://geant4-data.web.cern.ch/geant4-data/datasets/G4PII.1.3.tar.gz"

    tags = ['hep']

    maintainers = ['drbenmorgan']

    # Only versions relevant to Geant4 releases built by spack are added
    version('1.3', sha256='6225ad902675f4381c98c6ba25fc5a06ce87549aa979634d3d03491d6616e926')

    # use geant4-config for version info
    executables = [r'^geant4-config$']

    def install(self, spec, prefix):
        mkdirp(join_path(prefix.share, 'data'))
        install_path = join_path(prefix.share, 'data', 'G4PII{0}'
                                 .format(self.version))
        install_tree(self.stage.source_path, install_path)

    def setup_dependent_run_environment(self, env, dependent_spec):
        install_path = join_path(self.prefix.share, 'data', 'G4PII{0}'
                                 .format(self.version))
        env.set('G4PIIDATA', install_path)

    def url_for_version(self, version):
        """Handle version string."""
        return ("https://geant4-data.web.cern.ch/geant4-data/datasets/G4PII.1.3.tar.gz" % version)

    @classmethod
    def determine_spec_details(cls, prefix, exes_in_prefix):
        import os
        import re
        path = os.environ.get('G4PIIDATA', None)
        if not path:
            return
        pattern = '^(?P<prefix>.*?)/share/data/G4PII(?P<version>.*?)$'
        match = re.match(pattern, path)
        prefix = match.group('prefix')
        version = match.group('version')
        s = Spec.from_detection('g4pii@' + version)
        s.external_path = prefix
        return s

