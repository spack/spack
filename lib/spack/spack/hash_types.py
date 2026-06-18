# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Definitions that control how Spack creates Spec hashes."""

from typing import TYPE_CHECKING, Callable, List, Optional

import spack.deptypes as dt
import spack.repo

if TYPE_CHECKING:
    import spack.spec


class SpecHashDescriptor:
    """This class defines how hashes are generated on Spec objects.

    Spec hashes in Spack are generated from a serialized (e.g., with
    YAML) representation of the Spec graph.  The representation may only
    include certain dependency types, and it may optionally include a
    canonicalized hash of the package.py for each node in the graph.

    We currently use different hashes for different use cases."""

    __slots__ = "depflag", "package_hash", "name", "attr", "override"

    def __init__(
        self,
        depflag: dt.DepFlag,
        package_hash: bool,
        name: str,
        override: Optional[Callable[["spack.spec.Spec"], str]] = None,
    ) -> None:
        self.depflag = depflag
        self.package_hash = package_hash
        self.name = name
        self.attr = f"_{name}"
        # Allow spec hashes to have an alternate computation method
        self.override = override

    def __call__(self, spec: "spack.spec.Spec") -> str:
        """Run this hash on the provided spec."""
        return spec.spec_hash(self)

    def __repr__(self) -> str:
        return (
            f"SpecHashDescriptor(depflag={self.depflag!r}, "
            f"package_hash={self.package_hash!r}, name={self.name!r}, override={self.override!r})"
        )


#: The DAG hash includes all inputs that can affect how a package is built.
dag_hash = SpecHashDescriptor(
    depflag=dt.BUILD | dt.LINK | dt.RUN | dt.TEST, package_hash=True, name="hash"
)


def _content_hash_override(spec: "spack.spec.Spec") -> str:
    pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)
    pkg = pkg_cls(spec)
    return pkg.content_hash()


#: Package hash used as part of dag hash
package_hash = SpecHashDescriptor(
    depflag=0, package_hash=True, name="package_hash", override=_content_hash_override
)


# Deprecated hash types, no longer used, but needed to understand old serialized
# spec formats

full_hash = SpecHashDescriptor(
    depflag=dt.BUILD | dt.LINK | dt.RUN, package_hash=True, name="full_hash"
)


build_hash = SpecHashDescriptor(
    depflag=dt.BUILD | dt.LINK | dt.RUN, package_hash=False, name="build_hash"
)

HASHES: List["SpecHashDescriptor"] = [dag_hash, package_hash, full_hash, build_hash]
