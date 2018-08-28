##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
from spack.util.prefix import Prefix
from spack import *

import llnl.util.tty as tty
import os


class Jdk(Package):
    """The Java Development Kit (JDK) released by Oracle Corporation in the
    form of a binary product aimed at Java developers. Includes a complete JRE
    plus tools for developing, debugging, and monitoring Java applications."""

    homepage = "http://www.oracle.com/technetwork/java/javase/downloads/index.html"

    maintainers = ['justintoo']

    # Oracle requires that you accept their License Agreement in order
    # to access the Java packages in download.oracle.com. In order to
    # automate this process, we need to utilize these additional curl
    # command-line options. See:
    # http://stackoverflow.com/questions/10268583/how-to-automate-download-and-installation-of-java-jdk-on-linux
    curl_options = [
        '-j',  # junk cookies
        '-H',  # specify required License Agreement cookie
        'Cookie: oraclelicense=accept-securebackup-cookie'
    ]

    # To add the latest version, go to the homepage listed above,
    # click "JDK Download", click "Accept License Agreement", right-click the
    # Linux .tar.gz link, and select Copy Link Address. The checksum can be
    # found in a link above. The build number can be deciphered from the URL.
    # Alternatively, run `bin/java -version` after extracting. Replace '+'
    # symbol in version with '_', otherwise it will be interpreted as a variant
    version('10.0.1_10', 'ae8ed645e6af38432a56a847597ac61d4283b7536688dbab44ab536199d1e5a4', curl_options=curl_options,
            url='http://download.oracle.com/otn-pub/java/jdk/10.0.1+10/fb4372174a714e6b8c52526dc134031e/jdk-10.0.1_linux-x64_bin.tar.gz')
    version('1.8.0_172-b11', 'eda2945e8c02b84adbf78f46c37b71c1', curl_options=curl_options,
            url='http://download.oracle.com/otn-pub/java/jdk/8u172-b11/a58eab1ec242421181065cdc37240b08/jdk-8u172-linux-x64.tar.gz')
    version('1.8.0_141-b15', '8cf4c4e00744bfafc023d770cb65328c', curl_options=curl_options,
            url='http://download.oracle.com/otn-pub/java/jdk/8u141-b15/336fa29ff2bb4ef291e347e091f7f4a7/jdk-8u141-linux-x64.tar.gz')
    version('1.8.0_131-b11', '75b2cb2249710d822a60f83e28860053', curl_options=curl_options,
            url='http://download.oracle.com/otn-pub/java/jdk/8u131-b11/d54c1d3a095b4ff2b6607d096fa80163/jdk-8u131-linux-x64.tar.gz')
    version('1.8.0_92-b14', '65a1cc17ea362453a6e0eb4f13be76e4', curl_options=curl_options)
    version('1.8.0_73-b02', '1b0120970aa8bc182606a16bf848a686', curl_options=curl_options)
    version('1.8.0_66-b17', '88f31f3d642c3287134297b8c10e61bf', curl_options=curl_options)
    version('1.7.0_80-b0', '6152f8a7561acf795ca4701daa10a965', curl_options=curl_options)

    provides('java')
    provides('java@10', when='@10.0:10.999')
    provides('java@9',  when='@9.0:9.999')
    provides('java@8',  when='@1.8.0:1.8.999')
    provides('java@7',  when='@1.7.0:1.7.999')

    # FIXME:
    # 1. `extends('java')` doesn't work, you need to use `extends('jdk')`
    # 2. Packages cannot extend multiple packages, see #987
    # 3. Update `YamlFilesystemView.merge` to allow a Package to completely
    #    override how it is symlinked into a view prefix. Then, spack activate
    #    can symlink all *.jar files to `prefix.lib.ext`
    extendable = True

    @property
    def home(self):
        """Most of the time, ``JAVA_HOME`` is simply ``spec['java'].prefix``.
        However, if the user is using an externally installed JDK, it may be
        symlinked. For example, on macOS, the ``java`` executable can be found
        in ``/usr/bin``, but ``JAVA_HOME`` is actually
        ``/Library/Java/JavaVirtualMachines/jdk-10.0.1.jdk/Contents/Home``.
        Users may not know the actual installation directory and add ``/usr``
        to their ``packages.yaml`` unknowingly. Run ``java_home`` if it exists
        to determine exactly where it is installed. Specify which version we
        are expecting in case multiple Java versions are installed.
        See ``man java_home`` for more details."""

        prefix = self.prefix
        java_home = prefix.libexec.java_home
        if os.path.exists(java_home):
            java_home = Executable(java_home)
            version = str(self.version.up_to(2))
            prefix = java_home('--version', version, output=str).strip()
            prefix = Prefix(prefix)

        return prefix

    @property
    def libs(self):
        """Depending on the version number and whether the full JDK or just
        the JRE was installed, Java libraries can be in several locations:

        * ``lib/libjvm.so``
        * ``jre/lib/libjvm.dylib``

        Search recursively to find the correct library location."""

        return find_libraries(['libjvm'], root=self.home, recursive=True)

    @run_before('install')
    def macos_check(self):
        if self.spec.satisfies('platform=darwin'):
            msg = """\
Spack's JDK package only supports Linux. If you need to install JDK on macOS,
manually download the .dmg from:

    {0}

and double-click to install. Once JDK is installed, you can tell Spack where
to find it like so. To find the JDK installation directory, run:

    $ /usr/libexec/java_home

If you have multiple versions of JDK installed, you can specify a particular
version to search for with the --version flag. To find the exact version
number, run:

    $ java -version

If the version number contains a '+' symbol, replace it with '_', otherwise
Spack will think it is a variant. Add JDK as an external package by running:

    $ spack config edit packages

and adding entries for each installation:

    packages:
        jdk:
            paths:
                jdk@10.0.1_10:    /path/to/jdk/Home
                jdk@1.7.0_45-b18: /path/to/jdk/Home
            buildable: False""".format(self.homepage)

            tty.die(msg)

    def install(self, spec, prefix):
        install_tree('.', prefix)

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
