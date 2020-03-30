# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Quux(Package):
    """Toy package for testing dependencies"""

    homepage = "https://www.example.com"
    url      = "https://github.com/amundson/quux/archive/v3.0.0.tar.gz"

    version('3.0.0',
            sha256='b91bc96fb746495786bddac2c527039177499f2f76d3fa9dcf0b393859e68484')

    depends_on('garply')

    def install(self, spec, prefix):
        mkdirp('%s/bin' % self.stage.source_path)
        mkdirp(prefix.lib64)
        mkdirp('%s/quux' % prefix.include)
        copy('quux/quux_version_h.in', '%s/quux_version.h' %
             self.stage.source_path)
        filter_file('@QUUX_VERSION_MAJOR@', '3', '%s/quux_version.h' %
                    self.stage.source_path)
        filter_file('@QUUX_VERSION_MINOR@', '0', '%s/quux_version.h' %
                    self.stage.source_path)
        gpp = which('/usr/bin/g++')
        gpp('-Dquux_EXPORTS',
            '-I%s' % self.stage.source_path,
            '-I%s' % spec['garply'].prefix.include,
            '-O2', '-g', '-DNDEBUG', '-fPIC',
            '-o', 'quux.cc.o',
            '-c', 'quux/quux.cc')
        gpp('-Dquux_EXPORTS',
            '-I%s' % self.stage.source_path,
            '-I%s' % spec['garply'].prefix.include,
            '-O2', '-g', '-DNDEBUG', '-fPIC',
            '-o', 'quuxifier.cc.o',
            '-c', 'quux/quuxifier.cc')
        gpp('-fPIC', '-O2', '-g', '-DNDEBUG', '-shared',
            '-Wl,-soname,libquux.so', '-o', 'libquux.so', 'quux.cc.o',
            '-Wl,-rpath,%s:%s::::' % (prefix.lib64,
                                      spec['garply'].prefix.lib64),
            '%s/libgarply.so' % spec['garply'].prefix.lib64)
        gpp('-O2', '-g', '-DNDEBUG', '-rdynamic',
            'quuxifier.cc.o', '-o', 'quuxifier',
            '-Wl,-rpath,%s:%s::::' % (prefix.lib64,
                                      spec['garply'].prefix.lib64),
            'libquux.so',
            '%s/libgarply.so' % spec['garply'].prefix.lib64)
        copy('libquux.so', '%s/libquux.so' % prefix.lib64)
        copy('quuxifier', '%s/quuxifier' % prefix.lib64)
        copy('%s/quux/quux.h' % self.stage.source_path,
             '%s/quux/quux.h' % prefix.include)
