# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
import collections

import llnl.util.lang

import spack.paths
import spack.config
import spack.util.path
import spack.database
import spack.directory_layout
import spack.util.spack_yaml as syaml

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
    def __init__(self, root, path_scheme=None, hash_length=None):
        self.root = root

        upstream_dbs = retrieve_upstream_dbs()
        module_indices = read_module_indices()

        self.db = spack.database.Database(
            root, upstream_dbs=upstream_dbs)
        self.upstream_module_index = UpstreamModuleIndex(
            self.db, module_indices)
        self.layout = spack.directory_layout.YamlDirectoryLayout(
            root, hash_len=hash_length, path_scheme=path_scheme)

    def reindex(self):
        """Convenience function to reindex the store DB with its own layout."""
        return self.db.reindex(self.layout)


def _store():
    """Get the singleton store instance."""
    root = spack.config.get('config:install_tree', default_root)
    root = spack.util.path.canonicalize_path(root)

    #import pdb; pdb.set_trace()

    return Store(root,
                 spack.config.get('config:install_path_scheme'),
                 spack.config.get('config:install_hash_length'))


#: Singleton store instance
store = llnl.util.lang.Singleton(_store)

# convenience accessors for parts of the singleton store
root = llnl.util.lang.LazyReference(lambda: store.root)
db = llnl.util.lang.LazyReference(lambda: store.db)
layout = llnl.util.lang.LazyReference(lambda: store.layout)
upstream_module_index = llnl.util.lang.LazyReference(
    lambda: store.upstream_module_index)


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


ModuleIndexEntry = collections.namedtuple(
    'ModuleIndexEntry', ['path', 'use_name'])


def read_module_index(root):
    index_path = os.path.join(root, 'module-index.yaml')
    if not os.path.exists(index_path):
        return {}
    with open(index_path, 'r') as index_file:
        yaml_content = syaml.load(index_file)
        index = {}
        yaml_index = yaml_content['module_index']
        for dag_hash, module_properties in yaml_index.items():
            index[dag_hash] = ModuleIndexEntry(
                module_properties['path'],
                module_properties['use_name'])
        return index


def read_module_indices():
    other_spack_instances = spack.config.get(
        'upstreams') or {}

    module_indices = []

    for install_properties in other_spack_instances.values():
        module_type_to_index = {}
        module_type_to_root = install_properties.get('modules', {})
        for module_type, root in module_type_to_root.items():
            module_type_to_index[module_type] = read_module_index(root)
        module_indices.append(module_type_to_index)

    return module_indices


class UpstreamModuleIndex(object):
    def __init__(self, local_db, module_indices):
        self.local_db = local_db
        self.upstream_dbs = local_db.upstream_dbs
        self.module_indices = module_indices

    def upstream_module(self, spec, module_type):
        db_for_spec = self.local_db.db_for_spec_hash(spec.dag_hash())
        if db_for_spec in self.upstream_dbs:
            db_index = self.upstream_dbs.index(db_for_spec)
        elif db_for_spec:
            raise spack.error.SpackError(
                "Unexpected: {0} is installed locally".format(spec))
        else:
            raise spack.error.SpackError(
                "Unexpected: no install DB found for {0}".format(spec))
        module_index = self.module_indices[db_index]
        module_type_index = module_index.get(module_type, {})
        if not module_type_index:
            raise ModuleNotFoundError(
                "No {0} modules associated with the Spack instance where"
                " {1} is installed".format(module_type, spec))
        if spec.dag_hash() in module_type_index:
            return module_type_index[spec.dag_hash()]
        else:
            raise ModuleNotFoundError(
                "No module is available for upstream package {0}".format(spec))


class ModuleNotFoundError(spack.error.SpackError):
    """Raised when a module cannot be found for a spec"""
