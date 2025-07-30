# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from typing import Optional

from spack.package import PackageBase, join_url


class GNUMirrorPackage(PackageBase):
    gnu_mirror_path: Optional[str] = None
    base_mirrors = [
        "https://ftpmirror.gnu.org/",
        "https://ftp.gnu.org/gnu/",
        "http://ftpmirror.gnu.org/",
    ]

    @property
    def urls(self):
        if self.gnu_mirror_path is None:
            raise AttributeError(f"{self.__class__.__name__}: `gnu_mirror_path` missing")
        return [join_url(m, self.gnu_mirror_path, resolve_href=True) for m in self.base_mirrors]
