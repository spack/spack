import spack
import os

default_root = os.path.join(spack.paths.opt_path, 'spack')

chain_prefixes = spack.config.get('config:chain_prefixes',
                                  default=[])
parent_prefixes = []
for prefix in chain_prefixes:
    cprefix = spack.util.path.canonicalize_path(prefix)
    if cprefix == default_root:
        break
    parent_prefixes.append(cprefix)
parent_install_trees = []
for prefix in parent_prefixes:
    parent_install_trees.append(os.path.join(prefix, 'opt', 'spack'))
parent_install_trees.extend(spack.config.get('config:parent_install_trees',
                                             default=[]))
parent_stores = []
for parent_install_tree in parent_install_trees:
    parent_root = spack.util.path.canonicalize_path(parent_install_tree)
    if parent_root == default_root:
        break
    store = spack.store.Store(parent_root,
                              spack.config.get('config:install_path_scheme'),
                              spack.config.get('config:install_hash_length'))
    parent_stores.append(store)

parent_stores.append(spack.store.store)
