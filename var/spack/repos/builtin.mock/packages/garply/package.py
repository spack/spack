# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os


class Garply(Package):
    """Toy package for testing dependencies"""

    homepage = "https://www.example.com"
    url      = "https://github.com/gartung/garply/archive/v3.0.0.tar.gz"

    version('3.0.0',
            sha256='534ac8ba7a6fed7e8bbb543bd43ca04999e65337445a531bd296939f5ac2f33d')

    def install(self, spec, prefix):
        mkdirp(prefix.lib64)
        mkdirp('%s/garply' % prefix.include)
        copy('garply/garply_version_h.in', '%s/garply_version.h' %
             self.stage.source_path)
        filter_file('@GARPLY_VERSION_MAJOR@', '%s' % self.version[0],
                    '%s/garply_version.h' % self.stage.source_path)
        filter_file('@GARPLY_VERSION_MINOR@', '%s' % self.version[1:],
                    '%s/garply_version.h' % self.stage.source_path)
        gpp = which('/usr/bin/g++')
        gpp('-Dgarply_EXPORTS',
            '-I%s' % self.stage.source_path,
            '-O2', '-g', '-DNDEBUG', '-fPIC',
            '-o', 'garply.cc.o',
            '-c', '%s/garply/garply.cc' % self.stage.source_path)
        gpp('-Dgarply_EXPORTS',
            '-I%s' % self.stage.source_path,
            '-O2', '-g', '-DNDEBUG', '-fPIC',
            '-o', 'garplinator.cc.o',
            '-c', '%s/garply/garplinator.cc' % self.stage.source_path)
        gpp('-fPIC', '-O2', '-g', '-DNDEBUG', '-shared',
            '-Wl,-soname,libgarply.so', '-o', 'libgarply.so', 'garply.cc.o')
        gpp('-O2', '-g', '-DNDEBUG', '-rdynamic',
            'garplinator.cc.o', '-o', 'garplinator',
            '-Wl,-rpath,%s' % prefix.lib64,
            'libgarply.so')
        copy('libgarply.so', '%s/libgarply.so' % prefix.lib64)
        copy('garplinator', '%s/garplinator' % prefix.lib64)
        copy('%s/garply/garply.h' % self.stage.source_path,
             '%s/garply/garply.h' % prefix.include)
        mkdirp(prefix.bin)
        copy('garply_version.h', '%s/garply_version.h' % prefix.bin)
        os.symlink('%s/garplinator' % prefix.lib64,
                   '%s/garplinator' % prefix.bin)
