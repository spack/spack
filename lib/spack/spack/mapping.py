# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections.abc
from typing import Dict, List

import spack.spec


class ConcreteSpecsByHash(collections.abc.Mapping):
    """Mapping containing concrete specs keyed by DAG hash.

    The mapping is ensured to be consistent, i.e. if a spec in the mapping has a dependency with
    hash X, it is ensured to be the same object in memory as the spec keyed by X.
    """

    def __init__(self) -> None:
        self.data: Dict[str, spack.spec.Spec] = {}

    def __getitem__(self, dag_hash: str) -> spack.spec.Spec:
        return self.data[dag_hash]

    def add(self, spec: spack.spec.Spec) -> bool:
        """Adds a new concrete spec to the mapping. Returns True if the spec was just added,
        False if the spec was already in the mapping.

        Args:
            spec: spec to be added

        Raises:
            ValueError: if the spec is not concrete
        """
        if not spec.concrete:
            msg = (
                f"trying to store the non-concrete spec '{spec}' in a container "
                f"that only accepts concrete"
            )
            raise ValueError(msg)

        dag_hash = spec.dag_hash()
        if dag_hash in self.data:
            return False

        # Here we need to iterate on the input and rewire the copy.
        self.data[dag_hash] = spec.copy(deps=False)
        nodes_to_reconstruct = [spec]

        while nodes_to_reconstruct:
            input_parent = nodes_to_reconstruct.pop()
            container_parent = self.data[input_parent.dag_hash()]

            for edge in input_parent.edges_to_dependencies():
                input_child = edge.spec
                container_child = self.data.get(input_child.dag_hash())
                # Copy children that don't exist yet
                if container_child is None:
                    container_child = input_child.copy(deps=False)
                    self.data[input_child.dag_hash()] = container_child
                    nodes_to_reconstruct.append(input_child)

                # Rewire edges
                container_parent.add_dependency_edge(
                    dependency_spec=container_child, depflag=edge.depflag, virtuals=edge.virtuals
                )
        return True

    def query(self, spec: spack.spec.Spec) -> List[spack.spec.Spec]:
        """Returns a list of specs in the container matching the input query."""
        return [s for s in self.data.values() if s.satisfies(spec)]

    def delete(self, spec: spack.spec.Spec, transitive: bool = False) -> bool:
        """Deletes a concrete spec from the container. Returns True if the spec was deleted,
        False otherwise

        Args:
            spec: spec to be deleted
            transitive: if True deletes all the dependents, if False deletes
                only the spec iff it has no dependents
        Raises:
             ValueError: if the input spec is not concrete, or if the spec to be removed has
                dependents and 'transitive' is False.
        """
        if not spec.concrete:
            msg = f"cannot delete the non-concrete spec '{spec}'"
            raise ValueError(msg)

        dag_hash = spec.dag_hash()
        if dag_hash not in self.data:
            return False

        root = self.data[dag_hash]
        dependents = root.dependents()
        if dependents and not transitive:
            msg = (
                f"cannot remove {spec.short_spec}, since it is needed by "
                f"{', '.join(s.short_spec for s in dependents)}"
            )
            raise ValueError(msg)

        for parent in dependents:
            self.delete(parent, transitive=transitive)

        dependents = root.dependents()
        assert not dependents, "dependents should have been removed already"

        # Remove references from this node
        for dependency in root.dependencies():
            dependency._dependents.edges[root.name] = [
                x
                for x in dependency._dependents.edges[root.name]
                if x.parent.dag_hash() != dag_hash
            ]

        del self.data[dag_hash]
        return True

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self):
        return iter(self.data)
