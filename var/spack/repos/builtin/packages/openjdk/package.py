# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform
import re

from spack.util.prefix import Prefix

# If you need to add a new version, please be aware that:
#  - versions in the following dict are automatically added to the package
#  - version tuple must be in the form (checksum, url)
#  - checksum must be sha256
#  - package key must be in the form '{os}-{arch}' where 'os' is in the
#    format returned by platform.system() and 'arch' by platform.machine()

_versions = {
    '17.0.0_35': {
        'Linux-x86_64': ('6f1335d9a7855159f982dac557420397be9aa85f3f7bc84e111d25871c02c0c7', 'https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17%2B35/OpenJDK17-jdk_x64_linux_hotspot_17_35.tar.gz'),
        'Linux-aarch64': ('e08e6d8c84da28a2c49ccd511f8835c329fbdd8e4faff662c58fa24cca74021d', 'https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17%2B35/OpenJDK17-jdk_aarch64_linux_hotspot_17_35.tar.gz'),
        'Linux-ppc64le': ('2e58f76fd332b73f323e47c73d0a81b76739debab067e7a32ed6abd73fd64c57', 'https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17%2B35/OpenJDK17-jdk_ppc64le_linux_hotspot_17_35.tar.gz'),
        'Darwin-x86_64': ('e9de8b1b62780fe99270a5b30f0645d7a91eded60438bcf836a05fa7b93c182f', 'https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17%2B35/OpenJDK17-jdk_x64_mac_hotspot_17_35.tar.gz'),
        'Darwin-aarch64': ('910bb88543211c63298e5b49f7144ac4463f1d903926e94a89bfbf10163bbba1', 'https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17%2B35/OpenJDK17-jdk_aarch64_mac_hotspot_17_35.tar.gz')
    },
    '16.0.2': {
        'Linux-x86_64': ('6c714ded7d881ca54970ec949e283f43d673a142fda1de79b646ddd619da9c0c', 'https://download.java.net/java/GA/jdk16.0.2/d4a915d82b4c4fbb9bde534da945d746/7/GPL/openjdk-16.0.2_linux-x64_bin.tar.gz'),
        'Linux-aarch64': ('1ffb9c7748334945d9056b3324de3f797d906fce4dad86beea955153aa1e28fe', 'https://download.java.net/java/GA/jdk16.0.2/d4a915d82b4c4fbb9bde534da945d746/7/GPL/openjdk-16.0.2_linux-aarch64_bin.tar.gz'),
    },
    '11.0.12_7': {
        'Linux-x86_64': ('8770f600fc3b89bf331213c7aa21f8eedd9ca5d96036d1cd48cb2748a3dbefd2', 'https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.12%2B7/OpenJDK11U-jdk_x64_linux_hotspot_11.0.12_7.tar.gz'),
        'Linux-aarch64': ('105bdc12fcd54c551e8e8ac96bc82412467244c32063689c41cee29ceb7452a2', 'https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.12%2B7/OpenJDK11U-jdk_aarch64_linux_hotspot_11.0.12_7.tar.gz'),
        'Linux-ppc64le': ('234a9bafe029ea6cab5d46f9617b5d016a29faa187a42081d0e066f23647b7e5', 'https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.12%2B7/OpenJDK11U-jdk_ppc64le_linux_hotspot_11.0.12_7.tar.gz'),
        'Darwin-x86_64': ('13d056ee9a57bf2d5b3af4504c8f8cf7a246c4dff78f96b70dd05dad98075855', 'https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.12%2B7/OpenJDK11U-jdk_x64_mac_hotspot_11.0.12_7.tar.gz')
    },
    '11.0.9.1_1': {
        'Linux-ppc64le': ('d94b6b46a14ab0974b1c1b89661741126d8cf8a0068b471b8f5fa286a71636b1', 'https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.9.1%2B1/OpenJDK11U-jdk_ppc64le_linux_hotspot_11.0.9.1_1.tar.gz')},
    '11.0.8_10': {
        'Linux-x86_64': ('6e4cead158037cb7747ca47416474d4f408c9126be5b96f9befd532e0a762b47', 'https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.8%2B10/OpenJDK11U-jdk_x64_linux_hotspot_11.0.8_10.tar.gz')},
    '11.0.0-2020-01-01': {
        'Linux-aarch64': ('05c7d9c90edacd853850fbb0f52f8aa482809d0452c599cb9fe0b28b3b4bf329', 'https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk11u-2020-01-01-06-13/OpenJDK11U-jdk_aarch64_linux_hotspot_2020-01-01-06-13.tar.gz')},
    '11.0.2': {
        'Linux-x86_64': ('99be79935354f5c0df1ad293620ea36d13f48ec3ea870c838f20c504c9668b57', 'https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz'),
        'Darwin-x86_64': ('f365750d4be6111be8a62feda24e265d97536712bc51783162982b8ad96a70ee', 'https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_osx-x64_bin.tar.gz')
    },
    '11.0.1': {
        'Linux-x86_64': ('7a6bb980b9c91c478421f865087ad2d69086a0583aeeb9e69204785e8e97dcfd', 'https://download.java.net/java/GA/jdk11/13/GPL/openjdk-11.0.1_linux-x64_bin.tar.gz'),
        'Darwin-x86_64': ('fa07eee08fa0f3de541ee1770de0cdca2ae3876f3bd78c329f27e85c287cd070', 'https://download.java.net/java/GA/jdk11/13/GPL/openjdk-11.0.1_osx-x64_bin.tar.gz')
    },
    '1.8.0_265-b01': {
        'Linux-x86_64': ('1285da6278f2d38a790a21148d7e683f20de0799c44b937043830ef6b57f58c4', 'https://github.com/AdoptOpenJDK/openjdk8-binaries/releases/download/jdk8u265-b01/OpenJDK8U-jdk_x64_linux_hotspot_8u265b01.tar.gz')},
    '1.8.0_191-b12': {
        'Linux-aarch64': ('8eee0aede947b804f9a5f49c8a38b52aace8a30a9ebd9383b7d06042fb5a237c', 'https://github.com/AdoptOpenJDK/openjdk8-binaries/releases/download/jdk8u191-b12/OpenJDK8U-jdk_aarch64_linux_hotspot_8u191b12.tar.gz')},
    '1.8.0_222-b10': {
        'Linux-x86_64': ('20cff719c6de43f8bb58c7f59e251da7c1fa2207897c9a4768c8c669716dc819', 'https://github.com/AdoptOpenJDK/openjdk8-binaries/releases/download/jdk8u222-b10_openj9-0.15.1/OpenJDK8U-jdk_x64_linux_openj9_8u222b10_openj9-0.15.1.tar.gz')},
    '1.8.0_202-b08': {
        'Linux-x86_64': ('533dcd8d9ca15df231a1eb392fa713a66bca85a8e76d9b4ee30975f3823636b7', 'https://github.com/AdoptOpenJDK/openjdk8-binaries/releases/download/jdk8u202-b08/OpenJDK8U-jdk_x64_linux_openj9_8u202b08_openj9-0.12.0.tar.gz')},
    '1.8.0_40-b25': {
        'Linux-x86_64': ('79e96dce03a14271040023231a7d0ae374b755d48adf68bbdaec30294e4e2b88', 'https://download.java.net/openjdk/jdk8u40/ri/jdk_ri-8u40-b25-linux-x64-10_feb_2015.tar.gz')},
}


class Openjdk(Package):
    """The free and opensource java implementation"""

    homepage = "https://jdk.java.net"
    preferred_version = "11.0.12_7"

    for ver, packages in _versions.items():
        key = "{0}-{1}".format(platform.system(), platform.machine())
        pkg = packages.get(key)
        if pkg:
            is_preferred = preferred_version == ver
            version(ver, sha256=pkg[0], url=pkg[1], preferred=is_preferred)

    provides('java@17', when='@17.0:17')
    provides('java@16', when='@16.0:16')
    provides('java@11', when='@11.0:11')
    provides('java@10', when='@10.0:10')
    provides('java@9', when='@9.0:9')
    provides('java@8', when='@1.8.0:1.8')

    conflicts('target=ppc64:', msg='openjdk is not available for ppc64 (big endian)')

    # FIXME:
    # 1. `extends('java')` doesn't work, you need to use `extends('openjdk')`
    # 2. Packages cannot extend multiple packages, see #987
    # 3. Update `YamlFilesystemView.merge` to allow a Package to completely
    #    override how it is symlinked into a view prefix. Then, spack activate
    #    can symlink all *.jar files to `prefix.lib.ext`
    extendable = True

    executables = ['^java$']

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('-version', output=str, error=str)

        # Make sure this is actually OpenJDK, not Oracle JDK
        if 'openjdk' not in output:
            return None

        match = re.search(r'\(build (\S+)\)', output)
        return match.group(1).replace('+', '_') if match else None

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

    def install(self, spec, prefix):
        top_dir = 'Contents/Home/' if platform.system() == "Darwin" else '.'
        install_tree(top_dir, prefix)

    def setup_run_environment(self, env):
        """Set JAVA_HOME."""

        env.set('JAVA_HOME', self.home)

    def setup_dependent_build_environment(self, env, dependent_spec):
        """Set JAVA_HOME and CLASSPATH.

        CLASSPATH contains the installation prefix for the extension and any
        other Java extensions it depends on."""

        env.set('JAVA_HOME', self.home)

        class_paths = []
        for d in dependent_spec.traverse(deptype=('build', 'run', 'test')):
            if d.package.extends(self.spec):
                class_paths.extend(find(d.prefix, '*.jar'))

        classpath = os.pathsep.join(class_paths)
        env.set('CLASSPATH', classpath)

    def setup_dependent_run_environment(self, env, dependent_spec):
        """Set CLASSPATH.

        CLASSPATH contains the installation prefix for the extension and any
        other Java extensions it depends on."""
        # For runtime environment set only the path for
        # dependent_spec and prepend it to CLASSPATH
        if dependent_spec.package.extends(self.spec):
            class_paths = find(dependent_spec.prefix, '*.jar')
            classpath = os.pathsep.join(class_paths)
            env.prepend_path('CLASSPATH', classpath)

    def setup_dependent_package(self, module, dependent_spec):
        """Allows spec['java'].home to work."""

        self.spec.home = self.home
