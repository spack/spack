import spack
import os
#: default installation root, relative to the Spack install path
default_root = os.path.join(spack.paths.opt_path, 'spack')

chain_prefixes = spack.config.get('config:chain_prefixes',
                                  default=[None])
parent_prefixes = []
for prefix in chain_prefixes:
    if prefix == default_root:
        break
    parent_prefixes.append(prefix)
parent_install_trees = spack.config.get('config:parent_install_trees',
                                        default=[os.path.join(prefix, 'opt',
                                                              'spack')
                                                 for prefix in parent_prefixes]
                                        )
if not isinstance(parent_install_trees, (list, tuple)):
    parent_install_trees = [parent_install_trees]
if parent_install_trees == [None]:
    parent_install_trees = []
parent_dbs = [None]
parent_layouts = [None]
for parent_install_tree in parent_install_trees:
    parent_root = spack.util.path.canonicalize_path(parent_install_tree)
    if parent_root == default_root:
        break
    parent_dbs.append(spack.database.Database(parent_root,
                                              parent_db=parent_dbs[-1]))
    parent_layouts.append(spack.directory_layout.YamlDirectoryLayout(
                          parent_root,
                          hash_len=spack.config.get(
                              'config:' +
                              'install_hash_length'
                          ),
                          path_scheme=spack.config.get(
                              'config:' +
                              'install_path_scheme'
                          ),
                          parent_layout=parent_layouts[-1]))
root = spack.config.get('config:install_tree', default_root)
root = spack.util.path.canonicalize_path(root)
db = spack.database.Database(root, parent_db=parent_dbs[-1])
