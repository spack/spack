# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os

class Corge(Package):
    """A toy package to test dependencies"""

    homepage = "https://www.example.com"
    url      = "https://github.com/gartung/corge/archive/v3.0.0.tar.gz"

    version('3.0.0',
            sha256='5058861c3b887511387c725971984cec665a8307d660158915a04d7786fed6bc')

    depends_on('quux')

    def install(self, spec, prefix):
        mkdirp(prefix.lib64)
        mkdirp('%s/corge' % prefix.include)
        copy('corge/corge_version_h.in', '%s/corge_version.h' %
             self.stage.source_path)
        filter_file('@CORGE_VERSION_MAJOR@', '%s' % self.version[0],
                    '%s/corge_version.h' % self.stage.source_path)
        filter_file('@CORGE_VERSION_MINOR@', '%s' % self.version[1:],
                    '%s/corge_version.h' % self.stage.source_path)
        gpp = which('/usr/bin/g++')
        gpp('-Dcorge_EXPORTS',
            '-I%s' % self.stage.source_path,
            '-I%s' % spec['quux'].prefix.include,
            '-I%s' % spec['garply'].prefix.include,
            '-O2', '-g', '-DNDEBUG', '-fPIC',
            '-o', 'corge.cc.o',
            '-c', 'corge/corge.cc')
        gpp('-Dcorge_EXPORTS',
            '-I%s' % self.stage.source_path,
            '-I%s' % spec['quux'].prefix.include,
            '-I%s' % spec['garply'].prefix.include,
            '-O2', '-g', '-DNDEBUG', '-fPIC',
            '-o', 'corgegator.cc.o',
            '-c', 'corge/corgegator.cc')
        gpp('-fPIC', '-O2', '-g', '-DNDEBUG', '-shared',
            '-Wl,-soname,libcorge.so', '-o', 'libcorge.so', 'corge.cc.o',
            '-Wl,-rpath,%s:%s::::' %
            (spec['quux'].prefix.lib64, spec['garply'].prefix.lib64),
            '%s/libquux.so' % spec['quux'].prefix.lib64,
            '%s/libgarply.so' % spec['garply'].prefix.lib64)
        gpp('-O2', '-g', '-DNDEBUG', '-rdynamic',
            'corgegator.cc.o', '-o', 'corgegator',
            '-Wl,-rpath,%s:%s:%s:::' % (prefix.lib64,
                                        spec['quux'].prefix.lib64,
                                        spec['garply'].prefix.lib64),
            'libcorge.so',
            '%s/libquux.so' % spec['quux'].prefix.lib64,
            '%s/libgarply.so' % spec['garply'].prefix.lib64)
        copy('corgegator', '%s/corgegator' % prefix.lib64)
        copy('libcorge.so', '%s/libcorge.so' % prefix.lib64)
        copy('%s/corge/corge.h' % self.stage.source_path,
             '%s/corge/corge.h' % prefix.include)
        mkdirp(prefix.bin)
        copy('corge_version.h', '%s/corge_version.h' % prefix.bin)
        os.symlink('%s/corgegator' % prefix.lib64, '%s/corgegator' % prefix.bin)
        os.symlink('%s/quuxifier' % spec['quux'].prefix.lib64,
                   '%s/quuxifier' % prefix.bin)
        os.symlink('%s/garplinator' % spec['garply'].prefix.lib64,
                   '%s/garplinator' % prefix.bin)
