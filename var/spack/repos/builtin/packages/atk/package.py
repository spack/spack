# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Atk(Package):
    """ATK provides the set of accessibility interfaces that are
       implemented by other toolkits and applications. Using the ATK
       interfaces, accessibility tools have full access to view and
       control running applications."""
    homepage = "https://developer.gnome.org/atk/"
    url      = "http://ftp.gnome.org/pub/gnome/sources/atk/2.28/atk-2.28.1.tar.xz"
    list_url = "http://ftp.gnome.org/pub/gnome/sources/atk"
    list_depth = 1

    version('2.28.1', 'dfb5e7474220afa3f4ca7e45af9f3a11')
    version('2.20.0', '5187b0972f4d3905f285540b31395e20')
    version('2.14.0', 'ecb7ca8469a5650581b1227d78051b8b')

    depends_on('meson', type='build', when='@2.28.0:')
    depends_on('glib')
    depends_on('gettext')
    depends_on('pkgconfig', type='build')
    depends_on('gobject-introspection')

    def url_for_version(self, version):
        """Handle gnome's version-based custom URLs."""
        url = 'http://ftp.gnome.org/pub/gnome/sources/atk'
        return url + '/%s/atk-%s.tar.xz' % (version.up_to(2), version)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.prepend_path("XDG_DATA_DIRS",
                               self.prefix.share)
        run_env.prepend_path("XDG_DATA_DIRS",
                             self.prefix.share)

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            meson('..', *std_meson_args)
            ninja('-v')
            ninja('install')

    @when('@:2.27')
    def install(self, spec, prefix):
        configure('--prefix={0}'.format(prefix))
        make()
        if self.run_tests:
            make('check')
        make('install')
        if self.run_tests:
            make('installcheck')
