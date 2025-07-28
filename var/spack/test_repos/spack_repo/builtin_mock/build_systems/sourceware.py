# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import Optional

from spack.package import PackageBase, join_url


class SourcewarePackage(PackageBase):
    sourceware_mirror_path: Optional[str] = None
    base_mirrors = [
        "https://sourceware.org/pub/",
        "https://mirrors.kernel.org/sourceware/",
        "https://ftp.gwdg.de/pub/linux/sources.redhat.com/",
    ]

    @property
    def urls(self):
        if self.sourceware_mirror_path is None:
            raise AttributeError(f"{self.__class__.__name__}: `sourceware_mirror_path` missing")
        return [
            join_url(m, self.sourceware_mirror_path, resolve_href=True) for m in self.base_mirrors
        ]
