# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Components that manage Spack's installation tree.

An install tree, or "build store" consists of two parts:

  1. A package database that tracks what is installed.
  2. A directory layout that determines how the installations
     are laid out.

The store contains all the install prefixes for packages installed by
Spack.  The simplest store could just contain prefixes named by DAG hash,
but we use a fancier directory layout to make browsing the store and
debugging easier.

"""
import contextlib
import os
import re
from typing import Union

import llnl.util.lang
import llnl.util.tty as tty

import spack.config
import spack.database
import spack.directory_layout
import spack.error
import spack.paths
import spack.util.path

#: default installation root, relative to the Spack install path
default_install_tree_root = os.path.join(spack.paths.opt_path, "spack")


def parse_install_tree(config_dict):
    """Parse config settings and return values relevant to the store object.

    Arguments:
        config_dict (dict): dictionary of config values, as returned from
            spack.config.get('config')

    Returns:
        (tuple): triple of the install tree root, the unpadded install tree
            root (before padding was applied), and the projections for the
            install tree

    Encapsulate backwards compatibility capabilities for install_tree
    and deprecated values that are now parsed as part of install_tree.
    """
    # The following two configs are equivalent, the first being the old format
    # and the second the new format. The new format is also more flexible.

    # config:
    #   install_tree: /path/to/root$padding:128
    #   install_path_scheme: '{name}-{version}'

    # config:
    #   install_tree:
    #     root: /path/to/root
    #     padding: 128
    #     projections:
    #       all: '{name}-{version}'

    install_tree = config_dict.get("install_tree", {})

    padded_length = False
    if isinstance(install_tree, str):
        tty.warn("Using deprecated format for configuring install_tree")
        unpadded_root = install_tree
        unpadded_root = spack.util.path.canonicalize_path(unpadded_root)
        # construct projection from previous values for backwards compatibility
        all_projection = config_dict.get(
            "install_path_scheme", spack.directory_layout.default_projections["all"]
        )

        projections = {"all": all_projection}
    else:
        unpadded_root = install_tree.get("root", default_install_tree_root)
        unpadded_root = spack.util.path.canonicalize_path(unpadded_root)

        padded_length = install_tree.get("padded_length", False)
        if padded_length is True:
            padded_length = spack.util.path.get_system_path_max()
            padded_length -= spack.util.path.SPACK_MAX_INSTALL_PATH_LENGTH

        projections = install_tree.get("projections", spack.directory_layout.default_projections)

        path_scheme = config_dict.get("install_path_scheme", None)
        if path_scheme:
            tty.warn(
                "Deprecated config value 'install_path_scheme' ignored"
                " when using new install_tree syntax"
            )

    # Handle backwards compatibility for padding
    old_pad = re.search(r"\$padding(:\d+)?|\${padding(:\d+)?}", unpadded_root)
    if old_pad:
        if padded_length:
            msg = "Ignoring deprecated padding option in install_tree root "
            msg += "because new syntax padding is present."
            tty.warn(msg)
        else:
            unpadded_root = unpadded_root.replace(old_pad.group(0), "")
            if old_pad.group(1) or old_pad.group(2):
                length_group = 2 if "{" in old_pad.group(0) else 1
                padded_length = int(old_pad.group(length_group)[1:])
            else:
                padded_length = spack.util.path.get_system_path_max()
                padded_length -= spack.util.path.SPACK_MAX_INSTALL_PATH_LENGTH

    unpadded_root = unpadded_root.rstrip(os.path.sep)

    if padded_length:
        root = spack.util.path.add_padding(unpadded_root, padded_length)
        if len(root) != padded_length:
            msg = "Cannot pad %s to %s characters." % (root, padded_length)
            msg += " It is already %s characters long" % len(root)
            tty.warn(msg)
    else:
        root = unpadded_root

    return (root, unpadded_root, projections)


class Store:
    """A store is a path full of installed Spack packages.

    Stores consist of packages installed according to a
    ``DirectoryLayout``, along with an index, or _database_ of their
    contents.  The directory layout controls what paths look like and how
    Spack ensures that each uniqe spec gets its own unique directory (or
    not, though we don't recommend that). The database is a signle file
    that caches metadata for the entire Spack installation.  It prevents
    us from having to spider the install tree to figure out what's there.

    Args:
        root (str): path to the root of the install tree
        unpadded_root (str): path to the root of the install tree without
            padding; the sbang script has to be installed here to work with
            padded roots
        path_scheme (str): expression according to guidelines in
            ``spack.util.path`` that describes how to construct a path to
            a package prefix in this store
        hash_length (int): length of the hashes used in the directory
            layout; spec hash suffixes will be truncated to this length
    """

    def __init__(self, root, unpadded_root=None, projections=None, hash_length=None):
        self.root = root
        self.unpadded_root = unpadded_root or root
        self.projections = projections
        self.hash_length = hash_length
        self.db = spack.database.Database(root, upstream_dbs=retrieve_upstream_dbs())
        self.layout = spack.directory_layout.DirectoryLayout(
            root, projections=projections, hash_length=hash_length
        )

    def reindex(self):
        """Convenience function to reindex the store DB with its own layout."""
        return self.db.reindex(self.layout)

    def serialize(self):
        """Return a pickle-able object that can be used to reconstruct
        a store.
        """
        return (self.root, self.unpadded_root, self.projections, self.hash_length)

    @staticmethod
    def deserialize(token):
        """Return a store reconstructed from a token created by
        the serialize method.

        Args:
            token: return value of the serialize method

        Returns:
            Store object reconstructed from the token
        """
        return Store(*token)


def _store():
    """Get the singleton store instance."""
    import spack.bootstrap

    config_dict = spack.config.get("config")
    root, unpadded_root, projections = parse_install_tree(config_dict)
    hash_length = spack.config.get("config:install_hash_length")

    return Store(
        root=root, unpadded_root=unpadded_root, projections=projections, hash_length=hash_length
    )


#: Singleton store instance
store: Union[Store, llnl.util.lang.Singleton] = llnl.util.lang.Singleton(_store)


def _store_root():
    return store.root


def _store_unpadded_root():
    return store.unpadded_root


def _store_db():
    return store.db


def _store_layout():
    return store.layout


# convenience accessors for parts of the singleton store
root = llnl.util.lang.LazyReference(_store_root)
unpadded_root = llnl.util.lang.LazyReference(_store_unpadded_root)
db = llnl.util.lang.LazyReference(_store_db)
layout = llnl.util.lang.LazyReference(_store_layout)


def reinitialize():
    """Restore globals to the same state they would have at start-up. Return a token
    containing the state of the store before reinitialization.
    """
    global store
    global root, unpadded_root, db, layout

    token = store, root, unpadded_root, db, layout

    store = llnl.util.lang.Singleton(_store)
    root = llnl.util.lang.LazyReference(_store_root)
    unpadded_root = llnl.util.lang.LazyReference(_store_unpadded_root)
    db = llnl.util.lang.LazyReference(_store_db)
    layout = llnl.util.lang.LazyReference(_store_layout)

    return token


def restore(token):
    """Restore the environment from a token returned by reinitialize"""
    global store
    global root, unpadded_root, db, layout
    store, root, unpadded_root, db, layout = token


def retrieve_upstream_dbs():
    other_spack_instances = spack.config.get("upstreams", {})

    install_roots = []
    for install_properties in other_spack_instances.values():
        install_roots.append(install_properties["install_tree"])

    return _construct_upstream_dbs_from_install_roots(install_roots)


def _construct_upstream_dbs_from_install_roots(install_roots, _test=False):
    accumulated_upstream_dbs = []
    for install_root in reversed(install_roots):
        upstream_dbs = list(accumulated_upstream_dbs)
        next_db = spack.database.Database(
            spack.util.path.canonicalize_path(install_root),
            is_upstream=True,
            upstream_dbs=upstream_dbs,
        )
        next_db._fail_when_missing_deps = _test
        next_db._read()
        accumulated_upstream_dbs.insert(0, next_db)

    return accumulated_upstream_dbs


def find(constraints, multiple=False, query_fn=None, **kwargs):
    """Return a list of specs matching the constraints passed as inputs.

    At least one spec per constraint must match, otherwise the function
    will error with an appropriate message.

    By default, this function queries the current store, but a custom query
    function can be passed to hit any other source of concretized specs
    (e.g. a binary cache).

    The query function must accept a spec as its first argument.

    Args:
        constraints (List[spack.spec.Spec]): specs to be matched against
            installed packages
        multiple (bool): if True multiple matches per constraint are admitted
        query_fn (Callable): query function to get matching specs. By default,
            ``spack.store.db.query``
        **kwargs: keyword arguments forwarded to the query function

    Return:
        List of matching specs
    """
    # Normalize input to list of specs
    if isinstance(constraints, str):
        constraints = [spack.spec.Spec(constraints)]

    matching_specs, errors = [], []
    query_fn = query_fn or spack.store.db.query
    for spec in constraints:
        current_matches = query_fn(spec, **kwargs)

        # For each spec provided, make sure it refers to only one package.
        if not multiple and len(current_matches) > 1:
            msg_fmt = '"{0}" matches multiple packages: [{1}]'
            errors.append(msg_fmt.format(spec, ", ".join([m.format() for m in current_matches])))

        # No installed package matches the query
        if len(current_matches) == 0 and spec is not any:
            msg_fmt = '"{0}" does not match any installed packages'
            errors.append(msg_fmt.format(spec))

        matching_specs.extend(current_matches)

    if errors:
        raise MatchError(
            message="errors occurred when looking for specs in the store",
            long_message="\n".join(errors),
        )

    return matching_specs


def specfile_matches(filename, **kwargs):
    """Same as find but reads the query from a spec file.

    Args:
        filename (str): YAML or JSON file from which to read the query.
        **kwargs: keyword arguments forwarded to "find"

    Return:
        List of matches
    """
    query = [spack.spec.Spec.from_specfile(filename)]
    return spack.store.find(query, **kwargs)


@contextlib.contextmanager
def use_store(store_or_path):
    """Use the store passed as argument within the context manager.

    Args:
        store_or_path: either a Store object ot a path to where the store resides

    Returns:
        Store object associated with the context manager's store
    """
    global store, db, layout, root, unpadded_root

    # Normalize input arguments
    temporary_store = store_or_path
    if not isinstance(store_or_path, Store):
        temporary_store = Store(store_or_path)

    # Swap the store with the one just constructed and return it
    _ = store.db
    original_store, store = store, temporary_store
    db, layout = store.db, store.layout
    root, unpadded_root = store.root, store.unpadded_root

    try:
        yield temporary_store
    finally:
        # Restore the original store
        store = original_store
        db, layout = original_store.db, original_store.layout
        root, unpadded_root = original_store.root, original_store.unpadded_root


class MatchError(spack.error.SpackError):
    """Error occurring when trying to match specs in store against a constraint"""
