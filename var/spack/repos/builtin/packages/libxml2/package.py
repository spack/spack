# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxml2(AutotoolsPackage):
    """Libxml2 is the XML C parser and toolkit developed for the Gnome
       project (but usable outside of the Gnome platform), it is free
       software available under the MIT License."""

    homepage = "http://xmlsoft.org"
    url      = "http://xmlsoft.org/sources/libxml2-2.9.8.tar.gz"

    version('2.9.8', 'b786e353e2aa1b872d70d5d1ca0c740d')
    version('2.9.4', 'ae249165c173b1ff386ee8ad676815f5')
    version('2.9.2', '9e6a9aca9d155737868b3dc5fd82f788')
    version('2.7.8', '8127a65e8c3b08856093099b52599c86')

    variant('python', default=False, description='Enable Python support')

    extends('python', when='+python',
            ignore=r'(bin.*$)|(include.*$)|(share.*$)|(lib/libxml2.*$)|'
            '(lib/xml2.*$)|(lib/cmake.*$)')
    depends_on('zlib')
    depends_on('xz')

    depends_on('pkgconfig', type='build')

    def configure_args(self):
        spec = self.spec

        args = ["--with-lzma=%s" % spec['xz'].prefix]

        if '+python' in spec:
            args.extend([
                '--with-python={0}'.format(spec['python'].home),
                '--with-python-install-dir={0}'.format(site_packages_dir)
            ])
        else:
            args.append('--without-python')

        return args

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.prepend_path('CPATH', self.prefix.include.libxml2)
        run_env.prepend_path('CPATH', self.prefix.include.libxml2)
