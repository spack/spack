# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Classes and functions to manage package tags"""
from typing import TYPE_CHECKING, Dict, List

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

    def update_package(self, pkg_name: str, repo: "spack.repo.Repo") -> None:
        """Updates a package in the tag index.

        Args:
            pkg_name: name of the package to be updated
        """
        pkg_cls = repo.get_pkg_class(pkg_name)

        # Remove the package from the list of packages, if present
        for pkg_list in self.tags.values():
            if pkg_name in pkg_list:
                pkg_list.remove(pkg_name)

        # Add it again under the appropriate tags
        for tag in getattr(pkg_cls, "tags", []):
            tag = tag.lower()
            if tag not in self.tags:
                self.tags[tag] = [pkg_cls.name]
            else:
                self.tags[tag].append(pkg_cls.name)


class TagIndexError(spack.error.SpackError):
    """Raised when there is a problem with a TagIndex."""
