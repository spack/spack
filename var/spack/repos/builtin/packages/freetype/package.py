# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Freetype(AutotoolsPackage):
    """FreeType is a freely available software library to render fonts.
    It is written in C, designed to be small, efficient, highly customizable,
    and portable while capable of producing high-quality output (glyph images)
    of most vector and bitmap font formats."""

    homepage = "https://www.freetype.org/index.html"
    url      = "http://download.savannah.gnu.org/releases/freetype/freetype-2.7.1.tar.gz"

    version('2.9.1', 'ec391504e55498adceb30baceebd147a6e963f636eb617424bcfc47a169898ce')
    version('2.7.1', '78701bee8d249578d83bb9a2f3aa3616')
    version('2.7',   '337139e5c7c5bd645fe130608e0fa8b5')
    version('2.5.3', 'cafe9f210e45360279c730d27bf071e9')

    depends_on('libpng')
    depends_on('bzip2')
    depends_on('pkgconfig', type='build')

    def configure_args(self):
        args = ['--with-harfbuzz=no']
        if self.spec.satisfies('@2.9.1:'):
            args.append('--enable-freetype-config')
        return args

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.prepend_path('CPATH', self.prefix.include.freetype2)
        run_env.prepend_path('CPATH', self.prefix.include.freetype2)
