# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DarshanUtil(Package):
    """Darshan (util) is collection of tools for parsing and summarizing log
    files produced by Darshan (runtime) instrumentation. This package is
    typically installed on systems (front-end) where you intend to analyze
    log files produced by Darshan (runtime)."""

    homepage = "http://www.mcs.anl.gov/research/projects/darshan/"
    url = "http://ftp.mcs.anl.gov/pub/darshan/releases/darshan-3.1.0.tar.gz"

    version('3.1.6', 'ce5b8f1e69d602edd4753b57258b57c1')
    version('3.1.0', '439d717323e6265b2612ed127886ae52')
    version('3.0.0', '732577fe94238936268d74d7d74ebd08')

    variant('bzip2', default=False, description="Enable bzip2 compression")
    depends_on('zlib')
    depends_on('bzip2', when="+bzip2", type=("build", "link", "run"))

    def install(self, spec, prefix):

        options = ['CC=%s' % self.compiler.cc,
                   '--with-zlib=%s' % spec['zlib'].prefix]

        with working_dir('spack-build', create=True):
            configure = Executable('../darshan-util/configure')
            configure('--prefix=%s' % prefix, *options)
            make()
            make('install')
