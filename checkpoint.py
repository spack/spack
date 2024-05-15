import inspect
import json
import os
import pathlib
import sys

import spack
import spack.environment as ev
import spack.traverse as traverse


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

def get_config_hashes(env):
    # packages.yaml
    # repos.yaml
    # concretize.yaml (could swap reuse behavior)
    # compilers.yaml (could change flags)
    # (not) config.yaml

    for section in ["packages", "repos", "concretize", "compilers"]:
        data = spack.config.get_config(section)
        # Possible issue: if I convert the retrieved section to yaml, will
        # all the lines have a consistent order?

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


if __name__ == "__main__":
    main()
