# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Definitions that control how Spack creates Spec hashes."""

from typing import List

import spack.deptypes as dt


class SpecHashDescriptor:
    """This class describes how a Spec node is serialized for a given hash type.

    Spec hashes in Spack are generated from a serialized (e.g., with
    YAML) representation of the Spec graph.  The representation may only
    include certain dependency types, and it may optionally include a
    canonicalized hash of the package.py for each node in the graph.

    Only ``dag_hash`` is computed from that representation. The other descriptors name values
    that are assigned (``package_hash``) or read from old spec files (``full_hash``,
    ``build_hash``)."""

    __slots__ = "depflag", "package_hash", "name", "attr"

    def __init__(self, depflag: dt.DepFlag, package_hash: bool, name: str) -> None:
        self.depflag = depflag
        self.package_hash = package_hash
        self.name = name
        self.attr = f"_{name}"

    def __repr__(self) -> str:
        return (
            f"SpecHashDescriptor(depflag={self.depflag!r}, "
            f"package_hash={self.package_hash!r}, name={self.name!r})"
        )


#: The DAG hash includes all inputs that can affect how a package is built.
dag_hash = SpecHashDescriptor(
    depflag=dt.BUILD | dt.LINK | dt.RUN | dt.TEST, package_hash=True, name="hash"
)


#: Package hash used as part of dag hash. It is assigned at concretization time by
#: spack.spec.assign_package_hashes, since computing it requires a package.
package_hash = SpecHashDescriptor(depflag=0, package_hash=True, name="package_hash")


# Deprecated hash types, no longer used, but needed to understand old serialized
# spec formats

full_hash = SpecHashDescriptor(
    depflag=dt.BUILD | dt.LINK | dt.RUN, package_hash=True, name="full_hash"
)


build_hash = SpecHashDescriptor(
    depflag=dt.BUILD | dt.LINK | dt.RUN, package_hash=False, name="build_hash"
)

HASHES: List["SpecHashDescriptor"] = [dag_hash, package_hash, full_hash, build_hash]
