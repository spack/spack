# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Classes and functions to manage package tags"""
from typing import TYPE_CHECKING, Dict, List, Set

import spack.error
import spack.util.spack_json as sjson

if TYPE_CHECKING:
    import spack.repo


class TagIndex:
    """Maps tags to list of package names."""

    def __init__(self) -> None:
        self.tags: Dict[str, List[str]] = {}

    def to_json(self, stream) -> None:
        sjson.dump({"tags": self.tags}, stream)

    @staticmethod
    def from_json(stream) -> "TagIndex":
        d = sjson.load(stream)

        if not isinstance(d, dict):
            raise TagIndexError("TagIndex data was not a dict.")

        if "tags" not in d:
            raise TagIndexError("TagIndex data does not start with 'tags'")

        r = TagIndex()
        for tag, packages in d["tags"].items():
            r.tags[tag] = packages
        return r

    def get_packages(self, tag: str) -> List[str]:
        """Returns all packages associated with the tag."""
        return self.tags.get(tag, [])

    def merge(self, other: "TagIndex") -> None:
        """Merge another tag index into this one.

        Args:
            other: tag index to be merged
        """
        for tag, pkgs in other.tags.items():
            if tag not in self.tags:
                self.tags[tag] = pkgs.copy()
            else:
                self.tags[tag] = sorted({*self.tags[tag], *pkgs})

    def update_packages(self, pkg_names: Set[str], repo: "spack.repo.Repo") -> None:
        """Updates packages in the tag index.

        Args:
            pkg_names: names of the packages to be updated
            repo: the repository to get package classes from
        """
        # Remove the packages from the list of packages, if present
        for pkg_list in self.tags.values():
            if pkg_names.isdisjoint(pkg_list):
                continue
            pkg_list[:] = [pkg for pkg in pkg_list if pkg not in pkg_names]

        # Add them again under the appropriate tags
        for pkg_name in pkg_names:
            pkg_cls = repo.get_pkg_class(pkg_name)
            for tag in getattr(pkg_cls, "tags", []):
                tag = tag.lower()
                if tag not in self.tags:
                    self.tags[tag] = [pkg_cls.name]
                else:
                    self.tags[tag].append(pkg_cls.name)


class TagIndexError(spack.error.SpackError):
    """Raised when there is a problem with a TagIndex."""
