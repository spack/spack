# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from typing import Optional

from spack.package import PackageBase, join_url


class SourceforgePackage(PackageBase):
    sourceforge_mirror_path: Optional[str] = None
    base_mirrors = [
        "https://prdownloads.sourceforge.net/",
        "https://freefr.dl.sourceforge.net/",
        "https://netcologne.dl.sourceforge.net/",
        "https://pilotfiber.dl.sourceforge.net/",
        "https://downloads.sourceforge.net/",
        "http://kent.dl.sourceforge.net/sourceforge/",
    ]

    @property
    def urls(self):
        if self.sourceforge_mirror_path is None:
            raise AttributeError(f"{self.__class__.__name__}: `sourceforge_mirror_path` missing")
        return [
            join_url(m, self.sourceforge_mirror_path, resolve_href=True) for m in self.base_mirrors
        ]
