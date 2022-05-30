# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AttributesFoo(BundlePackage):
    phases = ['install']
    version('1.0')

    variant('bar', default=False, description='Enable the Foo implementation of bar')
    variant('baz', default=False, description='Enable the Foo implementation of baz')

    provides('bar', when='+bar')
    provides('baz', when='+baz')

    def install(self, spec, prefix):
        def libname(basename):
            _prefix = '' if 'platform=windows' in spec else 'lib'
            if 'platform=windows' in spec:
                _suffix = '.lib'
            elif 'platform=darwin' in spec:
                _suffix = '.dylib'
            else:
                _suffix = '.so'
            return _prefix + basename + _suffix

        mkdirp(prefix.join('include'))
        touch(prefix.join('include/foo.h'))
        mkdirp(prefix.join('include/bar'))
        touch(prefix.join('include/bar/bar.h'))
        mkdirp(prefix.join('lib64'))
        touch(prefix.join('lib64/{}'.format(libname('Foo'))))
        touch(prefix.join('lib64/{}'.format(libname('FooBar'))))
        mkdirp(prefix.join('baz/include/baz'))
        touch(prefix.join('baz/include/baz/baz.h'))
        mkdirp(prefix.join('baz/lib'))
        touch(prefix.join('baz/lib/{}'.format(libname('FooBaz'))))

    # All headers provided by Foo
    @property
    def headers(self):
        return find_headers('foo', root=self.spec.root.include, recursive=False)

    # All libraries provided by Foo
    @property
    def libs(self):
        spec = self.spec
        lib_name = 'Foo' if 'platform=windows' in spec else 'libFoo'
        return find_libraries(lib_name, root=spec.prefix, recursive=True)

    # The header provided by the bar virutal package
    @property
    def bar_headers(self):
        return find_headers('bar/bar', root=self.spec.prefix.include, recursive=False)

    # The libary provided by the bar virtual package
    @property
    def bar_libs(self):
        spec = self.spec
        lib_name = 'FooBar' if 'platform=windows' in spec else 'libFooBar'
        return find_libraries(lib_name, root=spec.prefix, recursive=True)

    # The baz virtual package root
    @property
    def baz_root(self):
        return self.spec.prefix.join('baz')

    # The header provided by the baz virtual package
    @property
    def baz_headers(self):
        return find_headers('baz/baz', root=self.baz_root.include, recursive=False)

    # The library provided by the baz virtual package
    @property
    def baz_libs(self):
        spec = self.spec
        lib_name = 'FooBaz' if 'platform=windows' in spec else 'libFooBaz'
        return find_libraries(lib_name, root=self.baz_root, recursive=True)
