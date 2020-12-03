# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Podio(CMakePackage):
    """PODIO, or plain-old-data I/O, is a C++ library to support the creation
    and handling of data models in particle physics."""

    homepage = "https://github.com/AIDASoft/podio"
    url      = "https://github.com/AIDASoft/podio/archive/v00-09-02.tar.gz"
    git      = "https://github.com/AIDASoft/podio.git"

    maintainers = ['vvolkl', 'drbenmorgan']

    tags = ["hep", "key4hep"]

    version('master', branch='master')
    version('0.13', sha256='e9cbd4e25730003d3706ad82e28b15cb5bdc524a78b0a26e90b89ea852101498')
    version('0.12.0', sha256='1729a2ce21e8b307fc37dfb9a9f5ae031e9f4be4992385cf99dba3e5fdf5323a')
    version('0.11.0', sha256='4b2765566a14f0ddece2c894634e0a8e4f42f3e44392addb9110d856f6267fb6')
    version('0.10.0', sha256='b5b42770ec8b96bcd2748abc05669dd3e4d4cc84f81ed57d57d2eda1ade90ef2')
    version('0.9.2', sha256='8234d1b9636029124235ef81199a1220968dcc7fdaeab81cdc96a47af332d240')
    version('0.9.0', sha256='3cde67556b6b76fd2d004adfaa3b3b6173a110c0c209792bfdb5f9353e21076f')
    version('0.8.0', sha256='9d035a7f5ebfae5279a17405003206853271af692f762e2bac8e73825f2af327')

    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release'))

    variant('sio', default=False,
            description='Build the SIO I/O backend')

    # cpack config throws an error on some systems
    patch('cpack.patch', when="@:0.10.0")
    patch('dictloading.patch', when="@0.10.0")

    depends_on('root@6.08.06: cxxstd=17')

    depends_on('cmake@3.8:', type='build')
    depends_on('python', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-jinja2@2.10.1:', type=('build', 'run'), when='@0.12.0:')
    depends_on('sio', type=('build', 'run'), when='+sio')

    conflicts('+sio', when='@:0.12', msg='sio support requires at least podio@0.13')

    def cmake_args(self):
        args = [
            self.define_from_variant('ENABLE_SIO', 'sio')
        ]
        return args

    def url_for_version(self, version):
        # podio releases are dashes and padded with a leading zero
        # the patch version is omitted when 0
        # so for example v01-12-01, v01-12 ...
        base_url = self.url.rsplit('/', 1)[0]
        major = str(version[0]).zfill(2)
        minor = str(version[1]).zfill(2)
        # handle the different cases for the patch version:
        # first case, no patch version is given in spack, i.e 0.1
        if len(version) == 2:
            url = base_url + "/v%s-%s.tar.gz" % (major, minor)
        # a patch version is specified in spack, i.e. 0.1.x ...
        elif len(version) == 3:
            patch = str(version[2]).zfill(2)
            # ... but it is zero, and not part of the ilc release url
            if version[2] == 0:
                url = base_url + "/v%s-%s.tar.gz" % (major, minor)
            # ... if it is non-zero, it is part  of the release url
            else:
                url = base_url + "/v%s-%s-%s.tar.gz" % (major, minor, patch)
        else:
            print('Error - Wrong version format provided')
            return
        return url

    def setup_run_environment(self, env):
        env.prepend_path('PYTHONPATH', self.prefix.python)
