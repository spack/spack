# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Xsd(MakefilePackage):
    """CodeSynthesis XSD is an open-source, cross-platform W3C XML Schema
    to C++ data binding compiler. It support in-memory and event-driven XML
    processing models and is available for a wide range of C++ compilers
    and platforms."""

    homepage = "https://www.codesynthesis.com"
    url      = "https://www.codesynthesis.com/download/xsd/4.0/xsd-4.0.0+dep.tar.bz2"

    version('4.0.0', 'ad3de699eb140e747a0a214462d95fc81a21b494')

    depends_on('xerces-c')
    depends_on('libtool', type='build')

    def install(self, spec, prefix):
        make('install', 'install_prefix=' + prefix)

    def setup_environment(self, spack_env, run_env):
        xercesc_lib_flags = self.spec['xerces-c'].libs.search_flags
        spack_env.append_flags('LDFLAGS', xercesc_lib_flags)

    def url_for_version(self, version):
        url = "https://www.codesynthesis.com/download/xsd/{0}/xsd-{1}+dep.tar.bz2"
        return url.format(version.up_to(2), version)
