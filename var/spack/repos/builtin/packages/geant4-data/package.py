# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import glob


class Geant4Data(Package):
    """An umbrella package to hold Geant4 data packages"""

    homepage = "http://geant4.cern.ch"
    url      = "http://geant4-data.web.cern.ch/geant4-data/ReleaseNotes/ReleaseNotes4.10.3.html"

    maintainers = ['drbenmorgan']

    version('10.03.p03', sha256='3e0d4d4e6854c8667d930fd5beaec09b7e6ec41f4847935e5d6a2720d0094b30', expand=False)
    version('10.04', sha256='f67fb899b99348a1a7e471a05f249f972e7e303c78238fc5f693b99968642255', expand=False)

    # geant4@10.03.p03
    depends_on("g4abla@3.0", when='@10.03.p03 ')
    depends_on("g4emlow@6.50", when='@10.03.p03 ')
    depends_on("g4ndl@4.5", when='@10.03.p03 ')
    depends_on("g4neutronxs@1.4", when='@10.03.p03 ')
    depends_on("g4saiddata@1.1", when='@10.03.p03 ')
    depends_on("g4ensdfstate@2.1", when='@10.03.p03 ')
    depends_on("g4photonevaporation@4.3.2", when='@10.03.p03 ')
    depends_on("g4pii@1.3", when='@10.03.p03 ')
    depends_on("g4radioactivedecay@5.1.1", when='@10.03.p03 ')
    depends_on("g4realsurface@1.0", when='@10.03.p03 ')
    depends_on("g4tendl@1.3", when='@10.03.p03 ')
    # geant4@10.04
    depends_on("g4abla@3.1", when='@10.04 ')
    depends_on("g4emlow@7.3", when='@10.04 ')
    depends_on("g4ndl@4.5", when='@10.04 ')
    depends_on("g4neutronxs@1.4", when='@10.04 ')
    depends_on("g4saiddata@1.1", when='@10.04 ')
    depends_on("g4ensdfstate@2.2", when='@10.04 ')
    depends_on("g4photonevaporation@5.2", when='@10.04 ')
    depends_on("g4pii@1.3", when='@10.04 ')
    depends_on("g4radioactivedecay@5.2", when='@10.04 ')
    depends_on("g4realsurface@2.1", when='@10.04 ')
    depends_on("g4tendl@1.3.2", when='@10.04 ')

    def install(self, spec, prefix):
        spec = self.spec
        version = self.version
        major = version[0]
        minor = version[1]
        if len(version) > 2:
            patch = version[-1]
        else:
            patch = 0
        data = 'Geant4-%s.%s.%s/data' % (major, minor, patch)
        datadir = join_path(spec.prefix.share, data)
        with working_dir(datadir, create=True):
            for d in glob.glob('%s/share/data/*' %
                               spec['g4abla'].prefix):
                os.symlink(d, os.path.basename(d))
            for d in glob.glob('%s/share/data/*' %
                               spec['g4emlow'].prefix):
                os.symlink(d, os.path.basename(d))
            for d in glob.glob('%s/share/data/*' %
                               spec['g4ndl'].prefix):
                os.symlink(d, os.path.basename(d))
            for d in glob.glob('%s/share/data/*' %
                               spec['g4saiddata'].prefix):
                os.symlink(d, os.path.basename(d))
            for d in glob.glob('%s/share/data/*' %
                               spec['g4neutronxs'].prefix):
                os.symlink(d, os.path.basename(d))
            for d in glob.glob('%s/share/data/*' %
                               spec['g4ensdfstate'].prefix):
                os.symlink(d, os.path.basename(d))
            for d in glob.glob('%s/share/data/*' %
                               spec['g4photonevaporation'].prefix):
                os.symlink(d, os.path.basename(d))
            for d in glob.glob('%s/share/data/*' %
                               spec['g4pii'].prefix):
                os.symlink(d, os.path.basename(d))
            for d in glob.glob('%s/share/data/*' %
                               spec['g4radioactivedecay'].prefix):
                os.symlink(d, os.path.basename(d))
            for d in glob.glob('%s/share/data/*' %
                               spec['g4realsurface'].prefix):
                os.symlink(d, os.path.basename(d))
            for d in glob.glob('%s/share/data/*' %
                               spec['g4tendl'].prefix):
                os.symlink(d, os.path.basename(d))

    def url_for_version(self, version):
        """Handle version string."""
        url = 'http://geant4-data.web.cern.ch/geant4-data/ReleaseNotes/'
        url = url + 'ReleaseNotes4.{0}.{1}.html'.format(version[0], version[1])
        return url
