# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class SharedMimeInfo(AutotoolsPackage):
    """Database of common MIME types."""

    homepage = "https://freedesktop.org/wiki/Software/shared-mime-info"
    url      = "http://freedesktop.org/~hadess/shared-mime-info-1.8.tar.xz"

    version('1.9', '45103889b91242850aa47f09325e798b')
    version('1.8', 'f6dcadce764605552fc956563efa058c')

    parallel = False

    depends_on('glib')
    depends_on('libxml2')
    depends_on('intltool', type='build')
    depends_on('gettext', type='build')
    depends_on('pkgconfig', type='build')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.prepend_path("XDG_DATA_DIRS",
                               self.prefix.share)
        run_env.prepend_path("XDG_DATA_DIRS",
                             self.prefix.share)
