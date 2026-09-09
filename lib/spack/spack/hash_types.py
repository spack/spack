# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Names of the hash values stored on Spec nodes."""

from typing import List


class SpecHashDescriptor:
    """Names a hash value stored on Spec nodes: its key in node dicts and its Spec attribute.

    Only ``dag_hash`` is computed, from the JSON serialization of a concrete spec's node dicts.
    The other descriptors name values that are assigned (``package_hash``) or read from old spec
    files (``full_hash``, ``build_hash``)."""

    __slots__ = "name", "attr"

    def __init__(self, name: str) -> None:
        self.name = name
        self.attr = f"_{name}"

    def __repr__(self) -> str:
        return f"SpecHashDescriptor(name={self.name!r})"


#: The DAG hash includes all inputs that can affect how a package is built.
dag_hash = SpecHashDescriptor(name="hash")


#: Package hash used as part of dag hash. It is assigned at concretization time by
#: spack.spec.assign_package_hashes, since computing it requires a package.
package_hash = SpecHashDescriptor(name="package_hash")


# Deprecated hash types, no longer used, but needed to understand old serialized
# spec formats

full_hash = SpecHashDescriptor(name="full_hash")


build_hash = SpecHashDescriptor(name="build_hash")

HASHES: List["SpecHashDescriptor"] = [dag_hash, package_hash, full_hash, build_hash]
