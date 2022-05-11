# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform
import re
import tempfile

from spack.package import *


class Texlive(AutotoolsPackage):
    """TeX Live is an easy (we hope) way to get up and running with the TeX
    document production system. It provides a comprehensive TeX system with
    binaries for most flavors of Unix, including GNU/Linux, macOS, and also
    Windows. It includes all the major TeX-related programs, macro packages,
    and fonts that are free software, including support for many languages
    around the world."""

    homepage = "https://www.tug.org/texlive"
    url = 'https://ftp.math.utah.edu/pub/tex/historic/systems/texlive/2020/texlive-20200406-source.tar.xz'
    base_url = 'http://ftp.math.utah.edu/pub/tex/historic/systems/texlive/{year}/texlive-{version}-{dist}.tar.xz'
    list_url = 'http://ftp.math.utah.edu/pub/tex/historic/systems/texlive'
    list_depth = 1

    # Below is the url for a binary distribution. This was originally how this
    # was distributed in Spack, but should be considered deprecated. Note that
    # the "live" version will pull down the packages so it requires an Internet
    # connection at install time and the package versions could change over
    # time. It is better to use a version built from tarballs, as defined with
    # the "releases" below.
    version('live', sha256='74eac0855e1e40c8db4f28b24ef354bd7263c1f76031bdc02b52156b572b7a1d',
            url='ftp://tug.org/historic/systems/texlive/2021/install-tl-unx.tar.gz')

    # Add information for new versions below.
    releases = [
        {
            'version': '20210325',
            'year': '2021',
            'sha256_source': '7aefd96608d72061970f2d73f275be5648ea8ae815af073016d3106acc0d584b',
            'sha256_texmf': 'ff12d436c23e99fb30aad55924266104356847eb0238c193e839c150d9670f1c',
        },
        {
            'version': '20200406',
            'year': '2020',
            'sha256_source': 'e32f3d08cbbbcf21d8d3f96f2143b64a1f5e4cb01b06b761d6249c8785249078',
            'sha256_texmf': '0aa97e583ecfd488e1dc60ff049fec073c1e22dfe7de30a3e4e8c851bb875a95',
        },
        {
            'version': '20190410',
            'year': '2019',
            'sha256_source': 'd2a29fef04e34dc3d2d2296c18995fc357aa7625e7a6bbf40fb92d83d3d0d7b5',
            'sha256_texmf': 'c2ec974abc98b91995969e7871a0b56dbc80dd8508113ffcff6923e912c4c402',
        },
    ]

    for release in releases:
        version(
            release['version'],
            sha256=release['sha256_source'],
            url=base_url.format(
                year=release['year'],
                version=release['version'],
                dist='source'
            )
        )

        resource(
            name='texmf',
            url=base_url.format(
                year=release['year'],
                version=release['version'],
                dist='texmf'
            ),
            sha256=release['sha256_texmf'],
            when='@{0}'.format(
                release['version']
            )
        )

    # The following variant is only for the "live" binary installation.
    # There does not seem to be a complete list of schemes.
    # Examples include:
    #   full scheme (everything)
    #   medium scheme (small + more packages and languages)
    #   small scheme (basic + xetex, metapost, a few languages)
    #   basic scheme (plain and latex)
    #   minimal scheme (plain only)
    # See:
    # https://www.tug.org/texlive/doc/texlive-en/texlive-en.html#x1-25025r6
    variant(
        'scheme',
        default='small',
        values=('minimal', 'basic', 'small', 'medium', 'full'),
        description='Package subset to install, only meaningful for "live" '
        'version'
    )

    depends_on('perl', type='build', when='@live')
    depends_on('pkgconfig', when='@2019:', type='build')

    depends_on('cairo+X', when='@2019:')
    depends_on('freetype', when='@2019:')
    depends_on('ghostscript', when='@2019:')
    depends_on('gmp', when='@2019:')
    depends_on('harfbuzz+graphite2', when='@2019:')
    depends_on('icu4c', when='@2019:')
    depends_on('libgd', when='@2019:')
    depends_on('libpaper', when='@2019:')
    depends_on('libpng', when='@2019:')
    depends_on('libxaw', when='@2019:')
    depends_on('libxt', when='@2019:')
    depends_on('mpfr', when='@2019:')
    depends_on('perl', when='@2019:')
    depends_on('pixman', when='@2019:')
    depends_on('poppler@:0.84', when='@2019:')
    depends_on('teckit', when='@2019:')
    depends_on('zlib', when='@2019:')
    depends_on('zziplib', when='@2019:')

    build_directory = 'spack-build'

    def tex_arch(self):
        tex_arch = '{0}-{1}'.format(platform.machine(),
                                    platform.system().lower())
        return tex_arch

    @when('@2019:')
    def configure_args(self):
        args = [
            '--bindir={0}'.format(join_path(self.prefix.bin, self.tex_arch())),
            '--disable-dvisvgm',
            '--disable-native-texlive-build',
            '--disable-static',
            '--enable-shared',
            '--with-banner-add= - Spack',
            '--dataroot={0}'.format(self.prefix),
            '--with-system-cairo',
            '--with-system-freetype2',
            '--with-system-gd',
            '--with-system-gmp',
            '--with-system-graphite2',
            '--with-system-harfbuzz',
            '--with-system-icu',
            '--with-system-libpaper',
            '--with-system-libpng',
            '--with-system-mpfr',
            '--with-system-pixman',
            '--with-system-poppler',
            '--with-system-teckit',
            '--with-system-zlib',
            '--with-system-zziplib',
        ]

        return args

    @run_after('install')
    def setup_texlive(self):
        if not self.spec.satisfies('@live'):
            mkdirp(self.prefix.tlpkg.TeXLive)
            install('texk/tests/TeXLive/*', self.prefix.tlpkg.TeXLive)

            with working_dir('spack-build'):
                make('texlinks')

            copy_tree('texlive-{0}-texmf'.format(self.version.string),
                      self.prefix)

            # Create and run setup utilities
            fmtutil_sys = Executable(join_path(self.prefix.bin,
                                               self.tex_arch(), 'fmtutil-sys'))
            mktexlsr = Executable(join_path(self.prefix.bin, self.tex_arch(),
                                            'mktexlsr'))
            mtxrun = Executable(join_path(self.prefix.bin, self.tex_arch(),
                                          'mtxrun'))
            mktexlsr()
            fmtutil_sys('--all')
            mtxrun('--generate')

        else:
            pass

    def setup_build_environment(self, env):
        env.prepend_path('PATH', join_path(self.prefix.bin, self.tex_arch()))

    def setup_run_environment(self, env):
        env.prepend_path('PATH', join_path(self.prefix.bin, self.tex_arch()))

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.setup_run_environment(env)

    @when('@live')
    def autoreconf(self, spec, prefix):
        touch('configure')

    @when('@live')
    def configure(self, spec, prefix):
        pass

    @when('@live')
    def build(self, spec, prefix):
        pass

    @when('@live')
    def install(self, spec, prefix):
        # The binary install needs a profile file to be present
        tmp_profile = tempfile.NamedTemporaryFile()
        tmp_profile.write("selected_scheme {0}".format(
            spec.variants['scheme']).encode())

        # Using texlive's mirror system leads to mysterious problems,
        # in lieu of being able to specify a repository as a variant, hardwire
        # a particular (slow, but central) one for now.
        _repository = 'https://ctan.math.washington.edu/tex-archive/systems/texlive/tlnet/'
        env = os.environ
        env['TEXLIVE_INSTALL_PREFIX'] = prefix
        perl = which('perl')
        scheme = spec.variants['scheme'].value
        perl('./install-tl', '-scheme', scheme,
             '-repository', _repository,
             '-portable', '-profile', tmp_profile.name)

        tmp_profile.close()

    executables = [r'^tex$']

    @classmethod
    def determine_version(cls, exe):
        # https://askubuntu.com/questions/100406/finding-the-tex-live-version
        # Thanks to @michaelkuhn that told how to reuse the package releases
        # variable.
        # Added 3 older releases: 2018 (CentOS-8), 2017 (Ubuntu-18.04), 2013 (CentOS-7).
        releases = cls.releases
        releases.extend([
            {
                'version': '20180414',
                'year': '2018',
            },
            {
                'version': '20170524',
                'year': '2017',
            },
            {
                'version': '20130530',
                'year': '2013',
            },
        ])
        # tex indicates the year only
        output = Executable(exe)('--version', output=str, error=str)
        match = re.search(r'TeX Live (\d+)', output)
        ver = match.group(1) if match else None
        # We search for the repo actual release
        if ver is not None:
            for release in releases:
                year = release['year']
                if year == ver:
                    ver = release['version']
                    break
        return ver
