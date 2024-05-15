import inspect
import os
import pathlib
import sys

import spack
import spack.environment as ev
import spack.traverse as traverse


def main():
    env = ev.active_environment()

    if not env:
        raise ValueError("An active env is required.")

    concrete_roots = list(y for x, y in env.concretized_specs())

    package_files = set()

    for spec in traverse.traverse_nodes(concrete_roots, key=traverse.by_dag_hash):
        if spec.external:
            continue

        inheritance_hierarchy = inspect.getmro(spec.package.__class__)

        cutoff = inheritance_hierarchy.index(spack.package_base.PackageBase)

        package_files.update(inspect.getfile(x) for x in inheritance_hierarchy[:cutoff])

    print("\n".join(package_files))

if __name__ == "__main__":
    main()
