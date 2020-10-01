# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
import six

import llnl.util.lang
import llnl.util.tty as tty

import spack.paths
import spack.config
import spack.util.path
import spack.database
import spack.directory_layout as dir_layout

#: default installation root, relative to the Spack install path
default_root = os.path.join(spack.paths.opt_path, 'spack')


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
        path_scheme (str): expression according to guidelines in
            ``spack.util.path`` that describes how to construct a path to
            a package prefix in this store
        hash_length (int): length of the hashes used in the directory
            layout; spec hash suffixes will be truncated to this length
    """
    def __init__(self, root, projections=None, hash_length=None):
        self.root = root
        self.db = spack.database.Database(
            root, upstream_dbs=retrieve_upstream_dbs())
        self.layout = dir_layout.YamlDirectoryLayout(
            root, projections=projections, hash_length=hash_length)

    def reindex(self):
        """Convenience function to reindex the store DB with its own layout."""
        return self.db.reindex(self.layout)


def _store():
    """Get the singleton store instance."""
    install_tree = spack.config.get('config:install_tree', {})

    if isinstance(install_tree, six.string_types):
        tty.warn("Using deprecated format for configuring install_tree")
        root = install_tree

        # construct projection from previous values for backwards compatibility
        all_projection = spack.config.get(
            'config:install_path_scheme',
            dir_layout.default_projections['all'])

        projections = {'all': all_projection}
    else:
        root = install_tree.get('root', default_root)
        root = spack.util.path.canonicalize_path(root)

        projections = install_tree.get(
            'projections', dir_layout.default_projections)

        path_scheme = spack.config.get('config:install_path_scheme', None)
        if path_scheme:
            tty.warn("Deprecated config value 'install_path_scheme' ignored"
                     " when using new install_tree syntax")

    return Store(root, projections,
                 spack.config.get('config:install_hash_length'))


#: Singleton store instance
store = llnl.util.lang.Singleton(_store)


def _store_root():
    return store.root


def _store_db():
    return store.db


def _store_layout():
    return store.layout


# convenience accessors for parts of the singleton store
root = llnl.util.lang.LazyReference(_store_root)
db = llnl.util.lang.LazyReference(_store_db)
layout = llnl.util.lang.LazyReference(_store_layout)


def retrieve_upstream_dbs():
    other_spack_instances = spack.config.get('upstreams', {})

    install_roots = []
    for install_properties in other_spack_instances.values():
        install_roots.append(install_properties['install_tree'])

    return _construct_upstream_dbs_from_install_roots(install_roots)


def _construct_upstream_dbs_from_install_roots(
        install_roots, _test=False):
    accumulated_upstream_dbs = []
    for install_root in reversed(install_roots):
        upstream_dbs = list(accumulated_upstream_dbs)
        next_db = spack.database.Database(
            install_root, is_upstream=True, upstream_dbs=upstream_dbs)
        next_db._fail_when_missing_deps = _test
        next_db._read()
        accumulated_upstream_dbs.insert(0, next_db)

    return accumulated_upstream_dbs
