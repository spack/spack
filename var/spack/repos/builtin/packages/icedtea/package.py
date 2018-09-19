##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import os


class Icedtea(AutotoolsPackage):
    """The IcedTea project provides a harness to build the source code from
    http://openjdk.java.net using Free Software build tools and adds a number
    of key features to the upstream OpenJDK codebase. IcedTea requires an
    existing IcedTea or OpenJDK install to build."""

    homepage = "http://icedtea.classpath.org/wiki/Main_Page"
    url      = "http://icedtea.wildebeest.org/download/source/icedtea-3.4.0.tar.gz"

    version('3.4.0',  'eba66765b92794495e16b83f23640872')

    variant('X', default=False, description="Build with GUI support.")
    variant('shenandoah', default=False,
            description="Build with the shenandoah gc. Only for version 3+")

    depends_on('pkgconfig', type='build')
    depends_on('gmake', type='build')
    depends_on('cups')
    depends_on('jdk', type='build')
    # X11 deps required for building even when headless
    depends_on('libx11', when='~X', type='build')
    depends_on('xproto', when='~X', type='build')
    depends_on('libxext', when='~X', type='build')
    depends_on('libxtst', when='~X', type='build')
    depends_on('libxi', when='~X', type='build')
    depends_on('libxt', when='~X', type='build')
    depends_on('libxinerama', when='~X', type='build')
    depends_on('libxrender', when='~X', type='build')
    depends_on('libxcomposite', when='~X', type='build')
    depends_on('libxau', when='~X', type='build')
    depends_on('libxdmcp', when='~X', type='build')
    depends_on('gtkplus', when='~X', type='build')

    depends_on('libx11', when='+X')
    depends_on('xproto', when='+X')
    depends_on('libxext', when='+X')
    depends_on('libxtst', when='+X')
    depends_on('libxi', when='+X')
    depends_on('libxt', when='+X')
    depends_on('libxinerama', when='+X')
    depends_on('libxrender', when='+X')
    depends_on('libxcomposite', when='+X')
    depends_on('libxau', when='+X')
    depends_on('libxdmcp', when='+X')
    depends_on('gtkplus', when='+X')

    depends_on('freetype@2:')
    depends_on('wget', type='build')
    depends_on('giflib')
    depends_on('libpng')
    depends_on('jpeg')
    depends_on('lcms')
    depends_on('zlib')
    depends_on('alsa-lib')

    provides('java')
    provides('java@8', when='@3.4.0:3.99.99')

    force_autoreconf = True

    resource(name='corba', placement='corba_src',
             sha512=('f0579608ab1342df231c4542dab1c40e648cda8e9780ea584fd476'
                     '79b07c93508cbfa85f0406d8aa8b9d528fc5bd99c9d41469568fbec'
                     '41a6456a13d914ac71c'),
             url='http://icedtea.wildebeest.org/download/drops/icedtea8/3.4.0/corba.tar.xz',
             when='@3.4.0')
    resource(name='hotspot', placement='hotspot_src',
             sha512=('29bc953d283f0a0a464fa150e2c4d71b0adaa29da67246843d230f3'
                     '70b5a20227fb40ef6a7e3b93f10b0cdec18b0cd2bbbceeaea3c9db4'
                     'd64c158cc23babbad2'),
             url='http://icedtea.wildebeest.org/download/drops/icedtea8/3.4.0/hotspot.tar.xz',
             when='@3.4.0')
    resource(name='jaxp', placement='jaxp_src',
             sha512=('ef3ed47815e6d15f40c5947fee1058c252ac673f70b6bf7c30505fa'
                     'a12fa5cbab8168d816abe7791dc88acec457744883db4c0af23fb21'
                     '66bbb709e870685bcd'),
             url='http://icedtea.wildebeest.org/download/drops/icedtea8/3.4.0/jaxp.tar.xz',
             when='@3.4.0')
    resource(name='jaxws', placement='jaxws_src',
             sha512=('867cac2919e715190596ae4f73fa42c6cba839ba48ae940adcef20a'
                     'bfb23ffeeaa2501c4aedc214b3595bc4e2a4eea9fa7e7cac62a3420'
                     'a11fb30a1f7edc9254'),
             url='http://icedtea.wildebeest.org/download/drops/icedtea8/3.4.0/jaxws.tar.xz',
             when='@3.4.0')
    resource(name='jdk', placement='jdk_src',
             sha512=('180d7b4435e465d68ed0b420b42dddc598c872075e225b8885ae183'
                     '3fa4ab5034ce5083c4dfba516a21b2d472321b37a01ba92793e17c7'
                     '8e9fddb1e254f12065'),
             url='http://icedtea.wildebeest.org/download/drops/icedtea8/3.4.0/jdk.tar.xz',
             when='@3.4.0')
    resource(name='langtools', placement='langtools_src',
             sha512=('0663f40b07de88cd7939557bf7fdb92077d7ca2132e369caefa82db'
                     '887261ea02102864d33ec0fef3b2c80dd366d25dbc1a95144139498'
                     'be581dfabe913e4312'),
             url='http://icedtea.wildebeest.org/download/drops/icedtea8/3.4.0/langtools.tar.xz',
             when='@3.4.0')
    resource(name='openjdk', placement='openjdk_src',
             sha512=('f3cca223bd39c0202dd1a65a38ca17024b6cb5c82d833946ec1b7d2'
                     '8d205833b4dd2dadde505a1c2384e3b28ff0d21a4f175e064b8ac82'
                     'aa8a07508e53cdc722'),
             url='http://icedtea.wildebeest.org/download/drops/icedtea8/3.4.0/openjdk.tar.xz',
             when='@3.4.0')
    resource(name='nashorn', placement='nashorn_src',
             sha512=('79b5095bab447d1911696bc1e328fb72c08764c0139cab14a28c0f6'
                     'c2e49a2d96bb06fbbb85523b2586672cb0f13709c3158823d5ac3f3'
                     'fe3f0f88402d3cb246'),
             url='http://icedtea.wildebeest.org/download/drops/icedtea8/3.4.0/nashorn.tar.xz',
             when='@3.4.0')
    resource(name='shenandoah', placement='shenandoah_src',
             sha512=('0f085e87c63679314ef322b3f4b854792d46539d5530dd75a7fd45b'
                     '8b6d663f58469be2808ea5fb4bf31f6c5369cb78f28e1599f748e19'
                     '31ba7040136306eb20'),
             url='http://icedtea.wildebeest.org/download/drops/icedtea8/3.4.0/shenandoah.tar.xz',
             when='@3.4.0')

    # FIXME:
    # 1. `extends('java')` doesn't work, you need to use `extends('icedtea')`
    # 2. Packages cannot extend multiple packages, see #987
    # 3. Update `YamlFilesystemView.merge` to allow a Package to completely
    #    override how it is symlinked into a view prefix. Then, spack activate
    #    can symlink all *.jar files to `prefix.lib.ext`
    extendable = True

    @property
    def home(self):
        """For compatibility with the ``jdk`` package, so that other packages
        can say ``spec['java'].home`` regardless of the Java provider."""
        return self.prefix

    def configure_args(self):
        os.environ['POTENTIAL_CXX'] = os.environ['CXX']
        os.environ['POTENTIAL_CC'] = os.environ['CC']
        os.environ['WGET'] = self.spec['wget'].command.path
        args = []
        if '~X' in self.spec:
            args.append('--enable-headless')
        if '+shenandoah' in self.spec:
            args.append('--with-hotspot-build=shenandoah')
            args.append('--with-hotspot-src-zip=' + self.stage[9].archive_file)
            args.append('--with-hotspot-checksum=no')
        else:
            args.append('--with-hotspot-src-zip=' + self.stage[2].archive_file)
            args.append('--with-hotspot-checksum=no')
        args += [
            '--with-corba-src-zip=' + self.stage[1].archive_file,
            '--with-cobra-checksum=no',
            '--with-jaxp-src-zip=' + self.stage[3].archive_file,
            '--with-jaxp-checksum=no',
            '--with-jaxws-src-zip=' + self.stage[4].archive_file,
            '--with-jaxws-checksum=no',
            '--with-jdk-src-zip=' + self.stage[5].archive_file,
            '--with-jdk-checksum=no',
            '--with-langtools-src-zip=' + self.stage[6].archive_file,
            '--with-langtools-checksum=no',
            '--with-openjdk-src-zip=' + self.stage[7].archive_file,
            '--with-openjdk-checksum=no',
            '--with-nashorn-src-zip=' + self.stage[8].archive_file,
            '--with-nashorn-checksum=no', '--disable-maintainer-mode'
            '--disable-downloading', '--disable-system-pcsc',
            '--disable-system-sctp', '--disable-system-kerberos',
            '--with-jdk-home=' + self.spec['jdk'].prefix
        ]
        return args

    def setup_environment(self, spack_env, run_env):
        """Set JAVA_HOME."""

        run_env.set('JAVA_HOME', self.home)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        """Set JAVA_HOME and CLASSPATH.

        CLASSPATH contains the installation prefix for the extension and any
        other Java extensions it depends on."""

        spack_env.set('JAVA_HOME', self.home)

        class_paths = []
        for d in dependent_spec.traverse(deptype=('build', 'run', 'test')):
            if d.package.extends(self.spec):
                class_paths.extend(find(d.prefix, '*.jar'))

        classpath = os.pathsep.join(class_paths)
        spack_env.set('CLASSPATH', classpath)

        # For runtime environment set only the path for
        # dependent_spec and prepend it to CLASSPATH
        if dependent_spec.package.extends(self.spec):
            class_paths = find(dependent_spec.prefix, '*.jar')
            classpath = os.pathsep.join(class_paths)
            run_env.prepend_path('CLASSPATH', classpath)

    def setup_dependent_package(self, module, dependent_spec):
        """Allows spec['java'].home to work."""

        self.spec.home = self.home
