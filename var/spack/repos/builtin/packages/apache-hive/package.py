# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
#     spack install apache-hive
#
# You can edit this file again by typing:
#
#     spack edit apache-hive
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class ApacheHive(Package):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://www-eu.apache.org/dist/hive/hive-3.1.1/apache-hive-3.1.1-bin.tar.gz"

    version('3.1.1', sha256='74db1859c3af4fcd39373c6caa99ff4c7e38dff3bcb9a198b7457c63b7e3c054')
    version('2.3.4', sha256='ce86d1c20b1004ef76b33feacf40aa7fc03b49de6299c424335fd7f6e875cea4')

    # FIXME: Add dependencies if required.
    depends_on('java', type='run')

    def install(self, spec, prefix):

        def install_dir(dirname):
            install_tree(dirname, join_path(prefix, dirname))

        install_dir('bin')
        install_dir('conf')
        install_dir('examples')
        install_dir('hcatalog')
        install_dir('jdbc')
        install_dir('lib')
        install_dir('scripts')
        install_dir('binary-package-licenses')
 #       install_file('LICENSE')
 #       install_file('NOTICE')
 #       install_file('RELEASE_NOTES.txt')
