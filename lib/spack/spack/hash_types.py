# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Definitions that control how Spack creates Spec hashes."""

import spack.dependency as dp

hashes = []


class SpecHashDescriptor(object):
    """This class defines how hashes are generated on Spec objects.

    Spec hashes in Spack are generated from a serialized (e.g., with
    YAML) representation of the Spec graph.  The representation may only
    include certain dependency types, and it may optionally include a
    canonicalized hash of the package.py for each node in the graph.

    We currently use different hashes for different use cases."""

    def __init__(self, deptype, package_hash, name, override=None):
        self.deptype = dp.canonical_deptype(deptype)
        self.package_hash = package_hash
        self.name = name
        hashes.append(self)
        # Allow spec hashes to have an alternate computation method
        self.override = override

    @property
    def attr(self):
        """Private attribute stored on spec"""
        return '_' + self.name


#: Default Hash descriptor, used by Spec.dag_hash() and stored in the DB.
dag_hash = SpecHashDescriptor(
    deptype=('link', 'run'), package_hash=False, name='hash')


#: Hash descriptor that includes build dependencies.
build_hash = SpecHashDescriptor(
    deptype=('build', 'link', 'run'), package_hash=False, name='build_hash')


#: Hash descriptor used only to transfer a DAG, as is, across processes
process_hash = SpecHashDescriptor(
    deptype=('build', 'link', 'run', 'test'),
    package_hash=False,
    name='process_hash'
)

#: Full hash used in build pipelines to determine when to rebuild packages.
full_hash = SpecHashDescriptor(
    deptype=('build', 'link', 'run'), package_hash=True, name='full_hash')


#: Package hash used as part of full hash
package_hash = SpecHashDescriptor(
    deptype=(), package_hash=True, name='package_hash',
    override=lambda s: s.package.content_hash())
