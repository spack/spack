# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Classes and functions to manage package tags"""
import collections
import copy
import sys

if sys.version_info >= (3, 5):
    from collections.abc import Mapping  # novm
else:
    from collections import Mapping

import spack.error
import spack.repo
import spack.util.spack_json as sjson


class TagIndex(Mapping):
    """Maps tags to list of packages."""

    def __init__(self):
        self._tag_dict = collections.defaultdict(list)

    @property
    def tags(self):
        return self._tag_dict

    def to_json(self, stream):
        sjson.dump({'tags': self._tag_dict}, stream)

    @staticmethod
    def from_json(stream):
        d = sjson.load(stream)

        if not isinstance(d, dict):
            raise TagIndexError("TagIndex data was not a dict.")

        if 'tags' not in d:
            raise TagIndexError("TagIndex data does not start with 'tags'")

        r = TagIndex()

        for tag, packages in d['tags'].items():
            r[tag].extend(packages)

        return r

    def __getitem__(self, item):
        return self._tag_dict[item]

    def __iter__(self):
        return iter(self._tag_dict)

    def __len__(self):
        return len(self._tag_dict)

    def copy(self):
        """Return a deep copy of this index."""
        clone = TagIndex()
        clone._tag_dict = copy.deepcopy(self._tag_dict)
        return clone

    def get_packages(self, tag):
        """Returns all packages associated with the tag."""
        return self.tags[tag] if tag in self.tags else []

    def merge(self, other):
        """Merge another tag index into this one.

        Args:
            other (TagIndex): tag index to be merged
        """
        other = other.copy()   # defensive copy.

        for tag in other.tags:
            if tag not in self.tags:
                self.tags[tag] = other.tags[tag]
                continue

            spkgs, opkgs = self.tags[tag], other.tags[tag]
            self.tags[tag] = sorted(list(set(spkgs + opkgs)))

    def update_package(self, pkg_name):
        """Updates a package in the tag index.

        Args:
            pkg_name (str): name of the package to be removed from the index

        """
        package = spack.repo.path.get(pkg_name)

        # Remove the package from the list of packages, if present
        for pkg_list in self._tag_dict.values():
            if pkg_name in pkg_list:
                pkg_list.remove(pkg_name)

        # Add it again under the appropriate tags
        for tag in getattr(package, 'tags', []):
            tag = tag.lower()
            self._tag_dict[tag].append(package.name)


class TagIndexError(spack.error.SpackError):
    """Raised when there is a problem with a TagIndex."""
