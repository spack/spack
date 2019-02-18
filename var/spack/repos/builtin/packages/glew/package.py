# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Glew(Package):
    """The OpenGL Extension Wrangler Library."""

    homepage = "http://glew.sourceforge.net/"
    url      = "https://sourceforge.net/projects/glew/files/glew/2.0.0/glew-2.0.0.tgz/download"

    version('2.0.0',  '2a2cd7c98f13854d2fcddae0d2b20411')

    depends_on("cmake", type='build')
    depends_on("gl")

    def install(self, spec, prefix):
        options = []
        options.extend(std_cmake_args)

        with working_dir('build'):
            cmake('./cmake/', *options)

            # https://github.com/Homebrew/legacy-homebrew/issues/22025
            # Note: This file is generated only after cmake is run
            filter_file(r'Requires: glu',
                        (''), '../glew.pc')

            make()
            make("install")
