# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

import spack.package


class GNUPackage(spack.package.PackageBase):
    """Mixin that takes care of setting url and mirrors for GNU packages."""
    gnu_path = None

    #: Primary URL to search for GNU packages
    base_url = 'https://ftp.gnu.org/gnu'

    #: List of GNU mirrors we'll use as a fall-back
    base_mirrors = [
        'https://ftpmirror.gnu.org/'
    ]

    @property
    def url(self):
        self._ensure_gnu_path_is_set_or_raise()
        return os.path.join(self.base_url, self.gnu_path)

    @property
    def mirrors(self):
        self._ensure_gnu_path_is_set_or_raise()
        return [
            os.path.join(m, self.gnu_path) for m in self.base_mirrors
        ]

    def _ensure_gnu_path_is_set_or_raise(self):
        if self.gnu_path is None:
            cls_name = type(self).__name__
            msg = '{0} must define a `gnu_path` attribute [none defined]'
            raise AttributeError(msg.format(cls_name))
