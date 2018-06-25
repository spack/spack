import spack
import os
#: default installation root, relative to the Spack install path
default_root = \
    spack.util.path.canonicalize_path(
        os.path.join(spack.paths.opt_path, 'spack'))

chain_prefixes = spack.config.get('config:chain_prefixes',
                                  default=[None])
parent_prefixes = []
for prefix in chain_prefixes:
    cprefix = spack.util.path.canonicalize_path(prefix)
    if cprefix == default_root:
        break
    parent_prefixes.append(cprefix)
parent_install_trees = []
default = []
for prefix in parent_prefixes:
    parent_install_trees.append(os.path.join(prefix, 'opt', 'spack'))
parent_install_trees.extend(spack.config.get('config:parent_install_trees',
                                        default=default))
parent_dbs = []
parent_layouts = []
for parent_install_tree in parent_install_trees:
    parent_root = spack.util.path.canonicalize_path(parent_install_tree)
    if parent_root == default_root:
        break
    if not parent_dbs:
        parent_dbs.append(spack.database.Database(parent_root))
        parent_layouts.append(spack.directory_layout.YamlDirectoryLayout(
                              parent_root,
                              hash_len=spack.config.get(
                                  'config:' +
                                  'install_hash_length'
                              ),
                              path_scheme=spack.config.get(
                                  'config:' +
                                  'install_path_scheme'
                              )))
    else:
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
