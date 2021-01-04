# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
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

The directory layout is currently hard-coded to be a YAMLDirectoryLayout,
so called because it stores build metadata within each prefix, in
`spec.yaml` files. In future versions of Spack we may consider allowing
install trees to define their own layouts with some per-tree
configuration.

"""
import os
import re
import six

import llnl.util.lang
import llnl.util.tty as tty

import spack.paths
import spack.config
import spack.util.path
import spack.database
import spack.directory_layout
import llnl.util.filesystem as fs

#: default installation root, relative to the Spack install path
default_install_tree_root = os.path.join(spack.paths.opt_path, 'spack')

install_root = None
active_upstream = None
init_upstream = None


def parse_install_tree():
    """Parse config settings and return values relevant to the store object.

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

    # Dictionaries of all install trees
    install_trees = spack.config.get('config:install_trees')
    shared_install_trees = spack.config.get('config:shared_install_trees')

    # Tests if non-default install root is specified
    if install_root:
        # Determines if install_root exists
        if install_root in install_trees:
            install_tree = install_trees[install_root]
        elif shared_install_trees and (install_root in shared_install_trees):
            install_tree = shared_install_trees[install_root]
        else:
            # TODO: provide the user an option to create a new install tree
            tty.die("Specified install tree does not exist: {0}"
                    .format(install_root))
    elif shared_install_trees:
        # If no install tree is specified and there are shared install trees,
        # then we are in user mode, and the install tree is in ~
        install_tree = install_trees['user']
    else:
        # If this is not a shared spack instance, then by default we will place
        # the install prefix inside the Spack tree
        if install_trees:
            install_tree = install_trees['spack-root']
        elif spack.config.get('config:install_tree'):
            install_tree = spack.config.get('config:install_tree')
        else:
            tty.die('No supported install tree formats found')

    padded_length = False
    if isinstance(install_tree, six.string_types):
        tty.warn("Using deprecated format for configuring install_tree")
        unpadded_root = install_tree
        unpadded_root = spack.util.path.canonicalize_path(unpadded_root)
        # construct projection from previous values for backwards compatibility
        all_projection = spack.config.get(
            'config:install_path_scheme',
            spack.directory_layout.default_projections['all'])

        projections = {'all': all_projection}
    else:
        unpadded_root = install_tree.get('root', default_install_tree_root)
        unpadded_root = spack.util.path.canonicalize_path(unpadded_root)

        padded_length = install_tree.get('padded_length', False)
        if padded_length is True:
            padded_length = spack.util.path.get_system_path_max()
            padded_length -= spack.util.path.SPACK_MAX_INSTALL_PATH_LENGTH

        projections = install_tree.get(
            'projections', spack.directory_layout.default_projections)

        path_scheme = spack.config.get('config:install_path_scheme', None)
        if path_scheme:
            tty.warn("Deprecated config value 'install_path_scheme' ignored"
                     " when using new install_tree syntax")

    # Handle backwards compatibility for padding
    old_pad = re.search(r'\$padding(:\d+)?|\${padding(:\d+)?}', unpadded_root)
    if old_pad:
        if padded_length:
            msg = "Ignoring deprecated padding option in install_tree root "
            msg += "because new syntax padding is present."
            tty.warn(msg)
        else:
            unpadded_root = unpadded_root.replace(old_pad.group(0), '')
            if old_pad.group(1) or old_pad.group(2):
                length_group = 2 if '{' in old_pad.group(0) else 1
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

    # Initializes upstream pointer if requested
    if init_upstream:
        if shared_install_trees:
            init_upstream_path = shared_install_trees[init_upstream]['root']
            initialize_upstream_pointer_if_unset(root, init_upstream_path)
        else:
            tty.die("Specified upstream must be defined"
                    " as shared install tree.")

    return (root, unpadded_root, projections)


class Store(object):
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
    def __init__(
            self, root, unpadded_root=None,
            projections=None, hash_length=None, active_upstream=None
    ):
        self.root = root
        self.unpadded_root = unpadded_root or root
        upstream_dbs = upstream_dbs_from_pointers(root)

        self.db = spack.database.Database(
            root, upstream_dbs=upstream_dbs)
        self.layout = spack.directory_layout.YamlDirectoryLayout(
            root, projections=projections, hash_length=hash_length)
        self.active_upstream = active_upstream

    def reindex(self):
        """Convenience function to reindex the store DB with its own layout."""
        return self.db.reindex(self.layout)


def _store():
    """Get the singleton store instance."""
    root, unpadded_root, projections = parse_install_tree()
    hash_length = spack.config.get('config:install_hash_length')

    return Store(root=root,
                 unpadded_root=unpadded_root,
                 projections=projections,
                 hash_length=hash_length)


#: Singleton store instance
store = llnl.util.lang.Singleton(_store)


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


def upstream_set(root):
    upstream_root_description = os.path.join(root, 'upstream-spack')
    return os.path.exists(upstream_root_description)


def initialize_upstream_pointer_if_unset(root, init_upstream_root):
    """Set the installation to point to the specified upstream."""
    if not os.path.exists(root):
        fs.mkdirp(root)
    upstream_root_description = os.path.join(root, 'upstream-spack')
    if not os.path.exists(upstream_root_description):
        with open(upstream_root_description, 'w') as f:
            f.write(init_upstream_root)


def upstream_install_roots(root):
    # Each installation root directory contains a file that points to the
    # upstream installation used (if any). This constructs a sequence of
    # upstream installations by recursively following these references.
    upstream_root_description = os.path.join(root, 'upstream-spack')
    install_roots = list()
    while os.path.exists(upstream_root_description):
        with open(upstream_root_description, 'r') as f:
            upstream_root = f.read()
            install_roots.append(upstream_root)
            upstream_root_description = os.path.join(
                upstream_root, 'upstream-spack')
    return install_roots


def upstream_dbs_from_pointers(root):
    return _construct_upstream_dbs_from_install_roots(
        upstream_install_roots(root))


def upstream_dbs_from_config():
    other_spack_instances = spack.config.get('upstreams', {})
    install_roots = []
    for install_properties in other_spack_instances.values():
        install_roots.append(spack.util.path.canonicalize_path(
                             install_properties['install_tree']))

    return _construct_upstream_dbs_from_install_roots(install_roots)


def _construct_upstream_dbs_from_install_roots(
        install_roots, _test=False):
    accumulated_upstream_dbs = []
    for install_root in reversed(install_roots):
        upstream_dbs = list(accumulated_upstream_dbs)
        next_db = spack.database.Database(
            install_root.strip(), is_upstream=True, upstream_dbs=upstream_dbs)
        next_db._fail_when_missing_deps = _test
        next_db._read()
        accumulated_upstream_dbs.insert(0, next_db)

    return accumulated_upstream_dbs
