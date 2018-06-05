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
import sys
from spack import *
from distutils.dir_util import copy_tree


class Git(AutotoolsPackage):
    """Git is a free and open source distributed version control
    system designed to handle everything from small to very large
    projects with speed and efficiency.
    """

    homepage = "http://git-scm.com"
    url      = "https://github.com/git/git/archive/v2.12.0.tar.gz"

    # In order to add new versions here, add a new list entry with:
    # * version: {version}
    # * md5: the md5sum of the v{version}.tar.gz
    # * md5_manpages: the md5sum of the corresponding manpage from
    #       https://www.kernel.org/pub/software/scm/git/git-manpages-{version}.tar.xz

    releases = [
        {
            'version': '2.17.1',
            'md5': 'e04bfbbe5f17a4faa9507c75b8505c13',
            'md5_manpages': 'f1d5dfc1459c9f2885f790c5af7473d1'
        },
        {
            'version': '2.17.0',
            'md5': '8e0f5253eef3abeb76bd9c55386d3bee',
            'md5_manpages': '1ce1ae78a559032810af8b455535935f'
        },
        {
            'version': '2.15.1',
            'md5': 'da59fc6baa55ab44684011e369af397d',
            'md5_manpages': '2cb428071c08c7df513cfc103610536e',
        },
        {
            'version': '2.14.1',
            'md5': 'e965a37b3d277f2e7e78f5b04de28e2a',
            'md5_manpages': 'da2e75ea3972b9e93fb47023e3bf1401',
        },
        {
            'version': '2.13.0',
            'md5': 'd0f14da0ef1d22f1ce7f7876fadcb39f',
            'md5_manpages': 'fda8d6d5314eb5a47e315405830f9970',
        },
        {
            'version': '2.12.2',
            'md5': 'f1a50c09ce8b5dd197f3c6c6d5ea8e75',
            'md5_manpages': '9358777e9a67e57427b03884c82311bd',
        },
        {
            'version': '2.12.1',
            'md5': 'a05c614c80ecd41e50699f1562e1130c',
            'md5_manpages': '8dfba0c9f51c6c23fb135d136c061c78',
        },
        {
            'version': '2.12.0',
            'md5': '11a440ce0ed02098adf554c797facfd3',
            'md5_manpages': '4d11e05068231e37d7e42935e9cc43a1',
        },
        {
            'version': '2.11.1',
            'md5': '2cf960f19e56f27248816809ae896794',
            'md5_manpages': 'ade1e458a34a89d03dda9a6de85976bd',
        },
        {
            'version': '2.11.0',
            'md5': 'c63fb83b86431af96f8e9722ebb3ca01',
            'md5_manpages': '72718851626e5b2267877cc2194a1ac9',
        },
        {
            'version': '2.9.3',
            'md5': 'b0edfc0f3cb046aec7ed68a4b7282a75',
            'md5_manpages': '337165a3b2bbe4814c73075cb6854ca2',
        },
        {
            'version': '2.9.2',
            'md5': '3ff8a9b30fd5c99a02e6d6585ab543fc',
            'md5_manpages': 'c4f415b4fc94cf75a1deb651ba769594',
        },
        {
            'version': '2.9.1',
            'md5': 'a5d806743a992300b45f734d1667ddd2',
            'md5_manpages': '2aa797ff70c704a563c910e04c0f620a',
        },
        {
            'version': '2.9.0',
            'md5': 'bf33a13c2adc05bc9d654c415332bc65',
            'md5_manpages': 'c840c968062251b768ba9852fd29054c',
        },
        {
            'version': '2.8.4',
            'md5': '86afb10254c3803894c9863fb5896bb6',
            'md5_manpages': '8340e772d60ccd04a5da88fa9c976dad',
        },
        {
            'version': '2.8.3',
            'md5': '0e19f31f96f9364fd247b8dc737dacfd',
            'md5_manpages': '553827e1b6c422ecc485499c1a1ae28d',
        },
        {
            'version': '2.8.2',
            'md5': '3d55550880af98f6e35c7f1d7c5aecfe',
            'md5_manpages': '33330463af27eb1238cbc2b4ca100b3a',
        },
        {
            'version': '2.8.1',
            'md5': '1308448d95afa41a4135903f22262fc8',
            'md5_manpages': '87bc202c6f6ae32c1c46c2dda3134ed1',
        },
        {
            'version': '2.8.0',
            'md5': 'eca687e46e9750121638f258cff8317b',
            'md5_manpages': 'd67a7db0f363e8c3b2960cd84ad0373f',
        },
        {
            'version': '2.7.3',
            'md5': 'fa1c008b56618c355a32ba4a678305f6',
            'md5_manpages': '97a525cca7fe38ff6bd7aaa4f0438896',
        },
        {
            'version': '2.7.1',
            'md5': 'bf0706b433a8dedd27a63a72f9a66060',
            'md5_manpages': '19881ca231f73dec91fb456d74943950',
        },
    ]

    for release in releases:
        version(release['version'], md5=release['md5'])
        resource(
            name='git-manpages',
            url="https://www.kernel.org/pub/software/scm/git/git-manpages-{0}.tar.xz".format(
                release['version']),
            md5=release['md5_manpages'],
            placement='git-manpages',
            when='@{0}'.format(release['version']))

    depends_on('curl')
    depends_on('expat')
    depends_on('gettext')
    depends_on('libiconv')
    depends_on('openssl')
    depends_on('pcre', when='@:2.13')
    depends_on('pcre+jit', when='@2.14:')
    depends_on('perl')
    depends_on('zlib')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    # See the comment in setup_environment re EXTLIBS.
    def patch(self):
        filter_file(r'^EXTLIBS =$',
                    '#EXTLIBS =',
                    'Makefile')

    def setup_environment(self, spack_env, run_env):
        # We use EXTLIBS rather than LDFLAGS so that git's Makefile
        # inserts the information into the proper place in the link commands
        # (alongside the # other libraries/paths that configure discovers).
        # LDFLAGS is inserted *before* libgit.a, which requires libintl.
        # EXTFLAGS is inserted *after* libgit.a.
        # This depends on the patch method above, which keeps the Makefile
        # from stepping on the value that we pass in via the environment.
        #
        # The test avoids failures when git is an external package.
        # In that case the node in the DAG gets truncated and git DOES NOT
        # have a gettext dependency.
        if 'gettext' in self.spec:
            spack_env.append_flags('EXTLIBS', '-L{0} -lintl'.format(
                self.spec['gettext'].prefix.lib))
            spack_env.append_flags('CFLAGS', '-I{0}'.format(
                self.spec['gettext'].prefix.include))

    def configure_args(self):
        spec = self.spec

        return [
            '--with-curl={0}'.format(spec['curl'].prefix),
            '--with-expat={0}'.format(spec['expat'].prefix),
            '--with-iconv={0}'.format(spec['libiconv'].prefix),
            '--with-libpcre={0}'.format(spec['pcre'].prefix),
            '--with-openssl={0}'.format(spec['openssl'].prefix),
            '--with-perl={0}'.format(spec['perl'].command.path),
            '--with-zlib={0}'.format(spec['zlib'].prefix),
        ]

    @run_after('configure')
    def filter_rt(self):
        if sys.platform == 'darwin':
            # Don't link with -lrt; the system has no (and needs no) librt
            filter_file(r' -lrt$', '', 'Makefile')

    def check(self):
        make('test')

    @run_after('install')
    def install_completions(self):
        copy_tree('contrib/completion', self.prefix.share)

    @run_after('install')
    def install_manpages(self):
        prefix = self.prefix

        with working_dir('git-manpages'):
            install_tree('man1', prefix.share.man.man1)
            install_tree('man5', prefix.share.man.man5)
            install_tree('man7', prefix.share.man.man7)
