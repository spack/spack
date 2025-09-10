# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Definitions that control how Spack creates Spec hashes."""
import base64
import hashlib
from typing import Any, Callable, Iterable, List, Optional

from spack.vendor.typing_extensions import TYPE_CHECKING

import spack.deptypes as dt
import spack.repo
import spack.traverse

if TYPE_CHECKING:
    import spack.spec

HASHES: List["SpecHashDescriptor"] = []


class SpecHashDescriptor:
    """This class defines how hashes are generated on Spec objects.

    Spec hashes in Spack are generated from a serialized (e.g., with
    YAML) representation of the Spec graph.  The representation may only
    include certain dependency types, and it may optionally include a
    canonicalized hash of the package.py for each node in the graph.

    We currently use different hashes for different use cases."""

    def __init__(
        self,
        depflag: dt.DepFlag,
        package_hash: bool,
        name: str,
        override: Optional[Callable[[Any], str]] = None,
    ):
        self.depflag = depflag
        self.package_hash = package_hash
        self.name = name
        HASHES.append(self)
        # Allow spec hashes to have an alternate computation method
        self.override = override

    @property
    def attr(self):
        """Private attribute stored on spec"""
        return "_" + self.name

    def __call__(self, spec):
        """Run this hash on the provided spec."""
        return spec.spec_hash(self)

    def __repr__(self):
        return (
            f"SpecHashDescriptor(depflag={self.depflag!r}, "
            f"package_hash={self.package_hash!r}, name={self.name!r}, override={self.override!r})"
        )


#: The DAG hash includes all inputs that can affect how a package is built.
dag_hash = SpecHashDescriptor(
    depflag=dt.BUILD | dt.LINK | dt.RUN | dt.TEST, package_hash=True, name="hash"
)


def _content_hash(spec):
    pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)
    pkg = pkg_cls(spec)
    return pkg.content_hash()


def _package_hash_override(spec) -> str:
    # Externals won't have a package hash, since their package.py file is not considered when
    # they are installed. The content hash of external's package.py file is instead considered
    # whenever they are dependencies of other packages.
    if spec.external:
        return "x" * 32

    hash_content = [_content_hash(s).encode("utf-8") for s in _package_hash_nodes(spec)]
    b32_hash = base64.b32encode(hashlib.sha256(bytes().join(hash_content)).digest()).lower()
    return b32_hash.decode("utf-8")


def _package_hash_nodes(spec) -> Iterable["spack.spec.Spec"]:
    # Sorting by name is fine. We won't have duplicate build dependencies on a single node
    build_deps = sorted(spec.dependencies(deptype=dt.BUILD), key=lambda x: x.name)
    for s in spack.traverse.traverse_nodes([spec, *build_deps], deptype=("link", "run")):
        yield s


#: Package hash used as part of dag hash
package_hash = SpecHashDescriptor(
    depflag=0, package_hash=True, name="package_hash", override=_package_hash_override
)


# Deprecated hash types, no longer used, but needed to understand old serialized
# spec formats

full_hash = SpecHashDescriptor(
    depflag=dt.BUILD | dt.LINK | dt.RUN, package_hash=True, name="full_hash"
)


build_hash = SpecHashDescriptor(
    depflag=dt.BUILD | dt.LINK | dt.RUN, package_hash=False, name="build_hash"
)
