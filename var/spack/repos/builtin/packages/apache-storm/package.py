# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install apache-storm
#
# You can edit this file again by typing:
#
#     spack edit apache-storm
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class ApacheStorm(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://www.apache.org/dyn/closer.lua/storm/apache-storm-1.2.2/apache-storm-1.2.2.tar.gz"

    version('1.2.2', sha256='af0cdde0f551a8b450b5ddad22779a19b30ac2a7bc8af94ad6e4d89526f83bfe')
    version('1.2.1', sha256='7b4a7b7d384f328c193c0942f0348ef5711e793d06a247d5bef9a9b8d7c3ed9c')
    version('1.1.3', sha256='a59287c390d911a6e93456682d383c66648366b68dfc52e039fb28a22acede20')

    # FIXME: Add dependencies if required.
    depends_on('java', type='run')

    def install(self, spec, prefix):

        def install_dir(dirname):
            install_tree(dirname, join_path(prefix, dirname))

        install_dir('bin')
        install_dir('conf')
        install_dir('examples')
        install_dir('external')
        install_dir('extlib')
        install_dir('extlib-daemon')
        install_dir('lib')
        install_dir('log4j2')
        install_dir('public')
        install_dir('toollib')
       
