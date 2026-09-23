# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Build graph and scheduling for the new installer.

Holds the :class:`BuildGraph` (the DAG of specs to install, with lazy build-dependency
expansion), :func:`schedule_builds` (per-spec lock acquisition and readiness selection), and the
:class:`DatabaseAction` hierarchy of pending DB writes. See :mod:`spack.installer` for the
overall design."""

import abc
import collections
from typing import Dict, FrozenSet, List, NamedTuple, Optional, Set, Tuple, Union

import spack.database
import spack.deptypes as dt
import spack.error
import spack.spec
import spack.store
import spack.traverse
import spack.util.lock
from spack.installer.base import InstallPolicy, JobServerBase


class DatabaseAction(abc.ABC):
    """Base class for objects that need to be persisted to the database."""

    __slots__ = ("spec", "prefix_lock")

    spec: spack.spec.Spec
    prefix_lock: Optional[spack.util.lock.Lock]

    @abc.abstractmethod
    def save_to_db(self, db: spack.database.Database) -> None:
        """Persist this action to the database."""

    def release_prefix_lock(self) -> None:
        if self.prefix_lock is not None:
            try:
                self.prefix_lock.release_write()
            except Exception:
                pass
        self.prefix_lock = None


class MarkExplicitAction(DatabaseAction):
    """Action to mark an already installed spec as explicitly installed."""

    __slots__ = ()

    def __init__(self, spec: "spack.spec.Spec") -> None:
        self.spec = spec
        self.prefix_lock = None

    def save_to_db(self, db: spack.database.Database) -> None:
        db._mark(self.spec, "explicit", True)


class AddSpecAction(DatabaseAction):
    """Action to add a successfully built spec to the database. Owns the prefix write lock from
    the moment the build finishes until the DB write (downgrade to read) or cleanup (release)."""

    __slots__ = ("explicit",)

    def __init__(
        self, spec: "spack.spec.Spec", explicit: bool, prefix_lock: Optional[spack.util.lock.Lock]
    ) -> None:
        self.spec = spec
        self.explicit = explicit
        self.prefix_lock = prefix_lock

    def save_to_db(self, db: spack.database.Database) -> None:
        db._add(self.spec, explicit=self.explicit)


class BuildGraph:
    """Represents the dependency graph for package installation."""

    def __init__(
        self,
        specs: List[spack.spec.Spec],
        root_policy: InstallPolicy,
        dependencies_policy: InstallPolicy,
        include_build_deps: bool,
        install_package: bool,
        install_deps: bool,
        store: spack.store.Store,
        overwrite_set: Optional[Set[str]] = None,
        tests: Union[bool, List[str], Set[str]] = False,
        explicit_set: Optional[Set[str]] = None,
        has_mirrors: bool = True,
    ):
        """Construct a build graph from the given specs. This includes only packages that need to
        be installed. Installed packages are pruned from the graph, and build dependencies are only
        included when necessary."""
        database = store.db
        self.roots = {s.dag_hash() for s in specs}
        self.nodes = {s.dag_hash(): s for s in specs}
        self.parent_to_child: Dict[str, Set[str]] = {}
        self.child_to_parent: Dict[str, Set[str]] = {}
        overwrite_set = overwrite_set or set()
        explicit_set = explicit_set or set()
        self.pruned: Set[str] = set()
        self.done: Set[str] = set()
        self.force_source: Set[str] = set()
        stack: List[Tuple[spack.spec.Spec, InstallPolicy]] = [
            (s, root_policy) for s in self.nodes.values()
        ]

        self.tests = tests

        with database.read_transaction():
            # Set the install prefix for each spec based on the db record or store layout
            for s in spack.traverse.traverse_nodes(specs):
                _, record = database.query_by_spec_hash(s.dag_hash())
                if record and record.path:
                    s.set_prefix(record.path)
                else:
                    s.set_prefix(store.layout.path_for_spec(s))

            # Build the graph and determine which specs to prune
            while stack:
                spec, install_policy = stack.pop()
                key = spec.dag_hash()
                _, record = database.query_by_spec_hash(key)
                depflag = self._base_deptypes(spec)

                # Conditionally include build dependencies. Don't prune installed specs
                # that need to be marked explicit so they flow through the DB write path.
                if record and record.installed and key not in overwrite_set:
                    # If it needs to be marked explicit, keep it in the graph (don't prune).
                    if key not in explicit_set or record.explicit:
                        self.pruned.add(key)
                elif (
                    install_policy == "source_only"
                    or include_build_deps
                    or (install_policy == "auto" and not has_mirrors)
                ):
                    depflag |= dt.BUILD

                dependencies = list(spec.dependencies(deptype=depflag))

                # For spliced specs built from source, add build_spec as a pseudo-dependency
                # so it gets built before the spliced spec.
                if spec.build_spec is not spec and key not in self.pruned and (depflag & dt.BUILD):
                    bs = spec.build_spec
                    bh = bs.dag_hash()
                    if bh not in self.pruned:
                        _, bs_record = database.query_by_spec_hash(bh)
                        if not (bs_record and bs_record.installed):
                            dependencies.append(bs)
                        else:
                            self.done.add(bh)

                self.parent_to_child[key] = {d.dag_hash() for d in dependencies}

                # Enqueue new dependencies
                for d in dependencies:
                    if d.dag_hash() in self.nodes:
                        continue
                    self.nodes[d.dag_hash()] = d
                    stack.append((d, dependencies_policy))

        # Construct reverse lookup from child to parent
        for parent, children in self.parent_to_child.items():
            for child in children:
                if child in self.child_to_parent:
                    self.child_to_parent[child].add(parent)
                else:
                    self.child_to_parent[child] = {parent}

        # If we're not installing the package itself, mark root specs for pruning too
        if not install_package:
            self.pruned.update(s.dag_hash() for s in specs)

        # Prune specs from the build graph. Their parents become parents of their children and
        # their children become children of their parents.
        for key in self.pruned:
            for parent in self.child_to_parent.get(key, ()):
                self.parent_to_child[parent].remove(key)
                self.parent_to_child[parent].update(self.parent_to_child.get(key, ()))
            for child in self.parent_to_child.get(key, ()):
                self.child_to_parent[child].remove(key)
                self.child_to_parent[child].update(self.child_to_parent.get(key, ()))
            self.parent_to_child.pop(key, None)
            self.child_to_parent.pop(key, None)
            self.nodes.pop(key, None)

        # Check that all prefixes to be created are unique.
        prefix_counts = collections.Counter(
            s.prefix for s in self.nodes.values() if not s.external
        )
        duplicate_prefixes = [p for p, count in prefix_counts.items() if count > 1]
        if duplicate_prefixes:
            raise spack.error.InstallError(
                "Install prefix collision: " + ", ".join(duplicate_prefixes)
            )

        # If we're not installing dependencies, verify that all remaining nodes in the build graph
        # after pruning are roots. If there are any non-root nodes, it means there are uninstalled
        # dependencies that we're not supposed to install.
        if not install_deps:
            non_root_spec = next((v for k, v in self.nodes.items() if k not in self.roots), None)
            if non_root_spec is not None:
                raise spack.error.InstallError(
                    f"Failed to install in package only mode: dependency {non_root_spec} is not "
                    "installed"
                )

    def _base_deptypes(self, spec: spack.spec.Spec) -> dt.DepFlag:
        """Returns the dependency types that are always eagerly traversed. These are LINK, RUN, and
        conditionally TEST, but excludes BUILD. Build deps are deferred until after a build cache
        miss."""
        deptypes = dt.LINK | dt.RUN
        if self.tests is True or (self.tests and spec.name in self.tests):
            deptypes |= dt.TEST
        return deptypes

    def enqueue_parents(self, dag_hash: str, pending_builds: List[str]) -> None:
        """After a spec is installed, remove it from the graph and enqueue any parents that are
        now ready to install.

        Args:
            dag_hash: The dag_hash of the spec that was just installed
            pending_builds: List to append parent specs that are ready to build
        """
        self.done.add(dag_hash)
        # Remove node and edges from the node in the build graph
        self.parent_to_child.pop(dag_hash, None)
        self.nodes.pop(dag_hash, None)
        parents = self.child_to_parent.pop(dag_hash, None)

        if not parents:
            return

        # Enqueue any parents and remove edges to the installed child
        for parent in parents:
            children = self.parent_to_child[parent]
            children.remove(dag_hash)
            if not children:
                pending_builds.append(parent)

    def has_unexpanded_build_deps(self, dag_hash: str) -> bool:
        return bool(self.get_unexpanded_build_deps(dag_hash))

    def get_unexpanded_build_deps(self, dag_hash: str) -> List["spack.spec.Spec"]:
        """Returns a list of unprocessed build deps for a spec."""
        spec = self.nodes[dag_hash]
        base_deptypes = self._base_deptypes(spec)
        unexpanded = []
        for edge in spec.edges_to_dependencies(depflag=dt.BUILD):
            if (edge.depflag & base_deptypes) == 0:
                unexpanded.append(edge.spec)
        if dag_hash in self.force_source and spec.build_spec is not spec:
            bh = spec.build_spec.dag_hash()
            if bh not in self.nodes and bh not in self.done and bh not in self.pruned:
                unexpanded.append(spec.build_spec)
        return unexpanded

    def expand_build_deps(
        self,
        spec_hashes: List[str],
        pending_builds: List[str],
        database: "spack.database.Database",
        dependencies_policy: InstallPolicy = "auto",
    ) -> List[str]:
        """Expand build dependencies for a list of specs after binary cache misses.

        Adds the spec's build deps and their transitive runtime deps to the graph. When
        ``dependencies_policy`` is ``"source_only"``, build deps of newly added specs are included
        immediately. Installed deps are skipped without adding edges.

        The caller must hold the database read lock and have called ``db._read()``.

        Returns the list of newly added dag hashes."""
        # Seed with tuples of (parent_hash, dep) for each to-be-expanded build dep
        stack = [(h, dep) for h in spec_hashes for dep in self.get_unexpanded_build_deps(h)]
        newly_added: List[str] = []

        while stack:
            parent_hash, dep = stack.pop()
            dep_hash = dep.dag_hash()

            # Skip installed deps
            if dep_hash in self.pruned or dep_hash in self.done:
                continue

            # If already in the graph (e.g. overwrite build in progress), add edge but don't
            # re-add node. This must be checked before the DB installed check, because an
            # overwrite build is installed in the DB but not yet done.
            if dep_hash in self.nodes:
                self.parent_to_child.setdefault(parent_hash, set()).add(dep_hash)
                self.child_to_parent.setdefault(dep_hash, set()).add(parent_hash)
                continue

            _, record = database.query_by_spec_hash(dep_hash)
            if record and record.installed:
                self.done.add(dep_hash)
                continue

            # Add forward/reverse edge
            self.parent_to_child.setdefault(parent_hash, set()).add(dep_hash)
            self.child_to_parent.setdefault(dep_hash, set()).add(parent_hash)

            # New node: add to graph and recurse into its link/run/test deps
            self.nodes[dep_hash] = dep
            self.parent_to_child.setdefault(dep_hash, set())
            newly_added.append(dep_hash)

            deptype = self._base_deptypes(dep)
            if dependencies_policy == "source_only":
                deptype |= dt.BUILD
            for child in dep.dependencies(deptype=deptype):
                stack.append((dep_hash, child))

        # Enqueue nodes that are ready (no uninstalled children)
        for h in newly_added:
            if not self.parent_to_child[h]:
                pending_builds.append(h)
        for dag_hash in spec_hashes:
            if not self.parent_to_child[dag_hash]:
                pending_builds.append(dag_hash)

        return newly_added


class ScheduleResult(NamedTuple):
    """Return value of :func:`schedule_builds`."""

    #: True if any pending builds were blocked on locks held by other processes.
    blocked: bool
    #: ``(dag_hash, lock)`` pairs where the write lock is held and the caller must start the build
    #: and eventually release the lock.
    to_start: List[Tuple[str, spack.util.lock.Lock]]
    #: ``(dag_hash, spec, lock)`` triples found already installed by another process; the read lock
    #: is held and the caller must add it to retained_read_locks.
    newly_installed: List[Tuple[str, spack.spec.Spec, spack.util.lock.Lock]]
    #: Actions to mark already installed specs explicit in the DB.
    to_mark_explicit: List[MarkExplicitAction]


def schedule_builds(
    pending: List[str],
    build_graph: BuildGraph,
    store: spack.store.Store,
    overwrite: Set[str],
    overwrite_time: float,
    capacity: int,
    needs_jobserver_token: bool,
    jobserver: JobServerBase,
    explicit: Set[str],
) -> ScheduleResult:
    """Try to schedule as many pending builds as possible.

    For each pending spec, attempts to acquire a non-blocking per-spec write lock. If the write
    lock times out, a read lock is tried as a fallback: a successful read lock means the first
    process finished and downgraded its write lock. If the DB confirms the spec is installed, it
    is captured as newly_installed; if the DB says it is not installed, the concurrent process was
    likely killed mid-build, and the spec is retried next iteration. Under both the DB read lock
    and the prefix lock, checks whether another process has already installed the spec. If so,
    captures it as newly_installed (caller enqueues parents) and keeps a read lock on the prefix
    to prevent concurrent uninstall. Otherwise, acquires a jobserver token if needed and adds the
    (dag_hash, lock) pair to to_start (caller launches the build).

    Args:
        pending: List of dag hashes pending installation; modified in-place.
        build_graph: The build dependency graph; used for node lookup and parent enqueueing.
        store: The local store for installs.
        overwrite: Set of dag hashes to overwrite even if already installed.
        overwrite_time: Timestamp (from time.time()) at which the overwrite install was requested.
            A spec in ``overwrite`` whose DB installation_time >= overwrite_time was installed by
            a concurrent process after our request started and should be treated as done.
        capacity: Maximum number of new builds to add to to_start in this call.
        needs_jobserver_token: True if a jobserver token is required for the first new build.
        jobserver: Jobserver for acquiring tokens.
        explicit: Set of dag hashes to mark explicit in the DB if found already installed.

    Returns:
        A :class:`ScheduleResult` with ``blocked``, ``to_start``, and ``newly_installed``
        fields; see :class:`ScheduleResult` for field semantics.
    """
    to_start: List[Tuple[str, spack.util.lock.Lock]] = []
    newly_installed: List[Tuple[str, spack.spec.Spec, spack.util.lock.Lock]] = []
    to_mark_explicit: List[MarkExplicitAction] = []
    blocked = True
    db = store.db

    # Acquire the DB read lock non-blocking; hold it throughout the loop so the in-memory snapshot
    # stays consistent while we acquire per-spec prefix locks.
    with db.try_read_transaction() as acquired:
        if not acquired:
            return ScheduleResult(blocked, to_start, newly_installed, to_mark_explicit)

        idx = 0
        while capacity and idx < len(pending):
            dag_hash = pending[idx]
            spec = build_graph.nodes[dag_hash]
            lock = store.prefix_locker.lock(spec)

            if lock.try_acquire_write():
                blocked = False
                have_write = True
            elif lock.try_acquire_read():
                have_write = False
            else:
                idx += 1
                continue

            # Check installed status under the DB read lock and prefix lock.
            upstream, record = db.query_by_spec_hash(dag_hash)

            # If the spec is already installed, treat it as done regardless of lock type.
            # A spec in the overwrite set is also treated as done if another process installed it
            # after our overwrite request was created (installation_time >= overwrite_time).
            if (
                record
                and record.installed
                and (dag_hash not in overwrite or record.installation_time >= overwrite_time)
            ):
                if have_write:
                    lock.downgrade_write_to_read()
                # keep the read lock (either downgraded or already a read lock)
                del pending[idx]
                newly_installed.append((dag_hash, spec, lock))
                # It's already installed, but needs to be marked as explicitly installed in the DB.
                if dag_hash in explicit and not record.explicit:
                    to_mark_explicit.append(MarkExplicitAction(spec))
                build_graph.enqueue_parents(dag_hash, pending)
                continue

            if not have_write:
                # If have to install but only got a read lock, try it in next iteration of the
                # event loop.
                lock.release_read()
                idx += 1
                continue

            # Write lock acquired: proceed with scheduling.

            # Allow local installs of specs that are referenced but uninstalled in an upstream db.
            # In edge cases where an upstream has forcibly uninstalled just a link dep, we cannot
            # fix the situation by installing it locally, because dependents in the upstream
            # reference the missing upstream path. However, we document that users should not
            # remove installed specs from upstreams, so it's a relatively safe assumption that
            # missing upstream specs were never installed or garbage collected build deps, and are
            # not referenced by absolute path in installed dependents.
            if upstream and record and not record.installed and not spec.external:
                spec.set_prefix(store.layout.path_for_spec(spec))

            # Defensively assert prefix invariants
            if not spec.external:
                if (
                    dag_hash in overwrite
                    and record
                    and record.installed
                    and record.path != spec.prefix
                ):
                    # Cannot do an overwrite install to a different prefix.
                    lock.release_write()
                    raise spack.error.InstallError(
                        f"Prefix mismatch in overwrite of {spec}: expected {record.path}, "
                        f"got {spec.prefix}"
                    )
                elif dag_hash not in overwrite and spec.prefix in db._installed_prefixes:
                    # Prevent install prefix collision with other specs.
                    lock.release_write()
                    raise spack.error.InstallError(
                        f"Cannot install {spec}: prefix {spec.prefix} already exists"
                    )

            # Acquire a jobserver token if needed. The first (implicit) job needs no token.
            if needs_jobserver_token and not jobserver.acquire(1):
                lock.release_write()
                break  # no tokens available right now; stop scheduling

            del pending[idx]
            to_start.append((dag_hash, lock))
            capacity -= 1
            needs_jobserver_token = True  # all subsequent jobs need a token

    return ScheduleResult(blocked, to_start, newly_installed, to_mark_explicit)


def _node_to_roots(roots: List[spack.spec.Spec]) -> Dict[str, FrozenSet[str]]:
    """Map each node in a graph to the set of root node DAG hashes that can reach it.

    Args:
        roots: List of root specs.

    Returns:
        A dictionary mapping each node's dag_hash to a frozenset of root dag_hashes.
    """
    node_to_roots: Dict[str, FrozenSet[str]] = {
        s.dag_hash(): frozenset([s.dag_hash()]) for s in roots
    }

    for edge in spack.traverse.traverse_edges(
        roots, order="topo", cover="edges", root=False, key=spack.traverse.by_dag_hash
    ):
        parent_roots = node_to_roots[edge.parent.dag_hash()]
        child_hash = edge.spec.dag_hash()
        existing = node_to_roots.get(child_hash)

        if existing is None:
            node_to_roots[child_hash] = parent_roots  # keep a reference if no mutation is needed
        elif not parent_roots.issubset(existing):
            node_to_roots[child_hash] = existing | parent_roots

    return node_to_roots
