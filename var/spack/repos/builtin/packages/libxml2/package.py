# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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

    depends_on('pkgconfig@0.9.0:', type='build')
    depends_on('libiconv')
    depends_on('zlib')
    depends_on('xz')

    depends_on('python+shared', when='+python')
    extends('python', when='+python',
            ignore=r'(bin.*$)|(include.*$)|(share.*$)|(lib/libxml2.*$)|'
            '(lib/xml2.*$)|(lib/cmake.*$)')

    # XML Conformance Test Suites
    # See http://www.w3.org/XML/Test/ for information
    resource(name='xmlts', url='http://www.w3.org/XML/Test/xmlts20080827.tar.gz',
             sha256='96151685cec997e1f9f3387e3626d61e6284d4d6e66e0e440c209286c03e9cc7')

    def configure_args(self):
        spec = self.spec

        args = ['--with-lzma={0}'.format(spec['xz'].prefix)]

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

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def import_module_test(self):
        if '+python' in self.spec:
            with working_dir('spack-test', create=True):
                python('-c', 'import libxml2')
