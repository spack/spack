# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os, glob

class Geant4Data(Package):
    """An umbrella package to hold Geant4 data packages"""

    homepage = "http://geant4.cern.ch"
    url      = "http://geant4-data.web.cern.ch/geant4-data/ReleaseNotes/ReleaseNotes4.10.3.html"

    version('10.03.p03', '2248ad436613897d9fad93bdb99d9446', expand=False)
    version('10.04', 'c49194b96e65ed4527d34d22a9860972', expand=False)

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
        datadir = join_path(spec.prefix.share,
                            'Geant4-%s.%s.%s/data' % (major, minor, patch)
        if '+data' not in self.spec:
            with working_dir(datadir,create=True):
                for d in glob.glob('%s/*' %
                                     spec['g4abla'].prefix.share.data):
                    os.symlink(rel, os.path.basename(d))
                for d in glob.glob('%s/*' %
                                     spec['g4emlow'].prefix.share.data):
                    os.symlink(rel, os.path.basename(d))
                for d in glob.glob('%s/*' %
                                     spec['g4ndl'].prefix.share.data):
                    os.symlink(rel, os.path.basename(d))
                for d in glob.glob('%s/*' %
                                     spec['g4saiddata'].prefix.share.data):
                    os.symlink(rel, os.path.basename(d))
                for d in glob.glob('%s/*' %
                                     spec['g4neutronxs'].prefix.share.data):
                    os.symlink(rel, os.path.basename(d))
                for d in glob.glob('%s/*' %
                                     spec['g4ensdfstate'].prefix.share.data):
                    os.symlink(rel, os.path.basename(d))
                for d in glob.glob('%s/*' %
                                     spec['g4photonevaporation'].prefix.share.data):
                    os.symlink(rel, os.path.basename(d))
                for d in glob.glob('%s/*' %
                                     spec['g4pii'].prefix.share.data):
                    os.symlink(d, os.path.basename(d))
                for d in glob.glob('%s/*' %
                                     spec['g4radioactivedecay'].prefix.share.data):
                    os.symlink(d, os.path.basename(d))
                for d in glob.glob('%s/*' %
                                     spec['g4realsurface'].prefix.share.data):
                    os.symlink(d, os.path.basename(d))
                for d in glob.glob('%s/*' %
                                     spec['g4tendl'].prefix.share.data):
                    os.symlink(d, os.path.basename(d))

    def url_for_version(self, version):
        """Handle version string."""
        return 'http://geant4-data.web.cern.ch/geant4-data/ReleaseNotes/ReleaseNotes4.{0}.{1}.html'.format(version[0],version[1])
