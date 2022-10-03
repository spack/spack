# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class TrivialInstallTestPackage(Package):
    """This package is a stub with a trivial install method.  It allows us
    to test the install and uninstall logic of spack."""

    homepage = "http://www.example.com/trivial_install"
    url = "http://www.unit-test-should-replace-this-url/trivial_install-1.0.tar.gz"

    variant('mkdir-share-dir', default=False)

    version("1.0", "0123456789abcdef0123456789abcdef")

    def install(self, spec, prefix):
        touch(join_path(prefix, "an_installation_file"))

        if '+mkdir-share-dir' in spec:
            share = join_path(prefix, "share")
            # mkdir() will fail if <prefix>/share/ already exists, which it will if the package
            # sources were installed (in <prefix>/share/pkg/src) before this install() is run.
            mkdir(share)
