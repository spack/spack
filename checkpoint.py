import inspect
import json
import os
import pathlib
import sys

import spack
import spack.environment as ev
import spack.traverse as traverse
import spack.util.crypto as crypto


class Checkpoint:
    def __init__(self, env):
        self.checksums = {}

    def paths_of_interest(self):
        return [
            self.env.manifest_path,
        ]

    def calculate_checksums(self):
        pass

    @staticmethod
    def read(path):
        pass

    def write(path):
        pass


def _get_config_scopes():
    return [x for x in spack.config.CONFIG.scopes.values()
            if not isinstance(x, spack.config.InternalConfigScope)]


def _checksum(path):
    fn = crypto.hash_fun_for_algo("sha256")
    return crypto.checksum(fn, path)


def get_config_hashes(env):
    # packages.yaml
    # repos.yaml
    # concretize.yaml (could swap reuse behavior)
    # compilers.yaml (could change flags)
    # (not) config.yaml

    cfg_paths = set()

    scopes = _get_config_scopes()
    for scope in scopes:
        for section in ["packages", "repos", "concretizer", "compilers"]:
            cfg_path = scope.get_section_filename(section)
            if cfg_path and os.path.exists(cfg_path):
                cfg_paths.add(cfg_path)


    path_to_hash = frozenset((x, _checksum(x)) for x in cfg_paths)
    return path_to_hash


def get_package_files(env):
    concrete_roots = list(y for x, y in env.concretized_specs())

    package_files = set()

    for spec in traverse.traverse_nodes(concrete_roots, key=traverse.by_dag_hash):
        if spec.external:
            continue

        inheritance_hierarchy = inspect.getmro(spec.package.__class__)

        cutoff = inheritance_hierarchy.index(spack.package_base.PackageBase)

        package_files.update(inspect.getfile(x) for x in inheritance_hierarchy[:cutoff])

    return package_files

def main():
    env = ev.active_environment()

    if not env:
        raise ValueError("An active env is required.")

    print("\n".join(get_package_files(env)))

    cfg_hashes = get_config_hashes(env)
    import pdb; pdb.set_trace()
    print(list(cfg_hashes)[:2])


if __name__ == "__main__":
    main()
