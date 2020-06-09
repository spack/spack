# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import platform

_versions = {
    '3.1.1': {
        'Linux-aarch64': '00f6eb11144525d426fe4dabcc9ddb5f6080cceb96b2cb77d2a55f0713412c20'},
    '3.1.0': {
        'Linux-aarch64': '42c540101ee8c50e4c90ba7a430a75459afb1802211e7d4a09ee694eb0157631'},
    '3.2.1': {
        'Linux-x86_64': 'f66a3a4115b8f16c1077d1a198a06854dbef0e4233291712ed08d0a10629ed37'},
    '3.1.3': {
        'Linux-x86_64': '1e8b7ca4e3911f8ec999595f71921390e9ad7a27255fbd36af1f3a1628b67e2b'},
    '2.10.0': {
        'Linux-x86_64': '131750c258368be4baff5d4a83b4de2cd119bda3774ed26d1d233b6fdf33f07f'},
    '2.9.2': {
        'Linux-x86_64': '3d2023c46b1156c1b102461ad08cbc17c8cc53004eae95dab40a1f659839f28a'},
    '2.8.5': {
        'Linux-x86_64': 'f9c726df693ce2daa4107886f603270d66e7257f77a92c9886502d6cd4a884a4'},
    '2.7.7': {
        'Linux-x86_64': 'd129d08a2c9dafec32855a376cbd2ab90c6a42790898cabbac6be4d29f9c2026'}
}


class Hadoop(Package):
    """The Apache Hadoop software library is a framework that
    allows for the distributed processing of large data sets
    across clusters of computers using simple programming models.
    """

    homepage = "http://hadoop.apache.org/"

    for ver, packages in _versions.items():
        key = "{0}-{1}".format(platform.system(), platform.machine())
        pkg = packages.get(key)

        if key == 'Linux-aarch64':
            fetch_url = 'https://github.com/apache/hadoop/archive/rel/release-{0}.tar.gz'
        if key == 'Linux-x86_64':
            fetch_url = 'https://www.apache.org/dist/hadoop/common/hadoop-{0}/hadoop-{0}.tar.gz'
        if pkg:
            version(ver, sha256=pkg, url=fetch_url.format(ver))

    depends_on('protobuf@2.5.0', when='target=aarch64:')
    depends_on('maven', type='build', when='target=aarch64:')
    depends_on('java@8', type=('build', 'run'), when='target=aarch64:')
    depends_on('java', type='run', when='target=x86_64:')
    depends_on('cmake', type='build', when='target=aarch64:')
    depends_on('libtirpc', when='target=aarch64:')
    depends_on('tar', type='build', when='target=aarch64:')

    @when('target=aarch64:')
    def setup_build_environment(self, env):
        lib_file_path = join_path(self.spec['libtirpc'].prefix.lib,
                                  'libtirpc.so')
        env.append_path('LDFLAGS', lib_file_path)
        env.prepend_path('CPATH', self.spec['libtirpc'].prefix.include.tirpc)

    @when('target=aarch64:')
    def install(self, spec, prefix):
        mvn = which('mvn')
        mvn('package', '-DskipTests', '-Pdist,native',
            '-Dtar', '-Dmaven.javadoc.skip=true')
        tar = which('tar')
        archive_path = join_path(self.stage.source_path,
                                 'hadoop-dist', 'target',
                                 'hadoop-{0}.tar.gz'.format(self.version))
        tar('-xvf', archive_path)
        hadoop_path = join_path(self.stage.source_path,
                                'hadoop-dist', 'target',
                                'hadoop-{0}'.format(self.version))
        with working_dir(hadoop_path):
            install_tree('.', prefix)

    @when('target=x86_64:')
    def install(self, spec, prefix):
        def install_dir(dirname):
            install_tree(dirname, join_path(prefix, dirname))
        install_dir('bin')
        install_dir('etc')
        install_dir('include')
        install_dir('lib')
        install_dir('libexec')
        install_dir('sbin')
        install_dir('share')
