# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Used to mark all specs in the currently active environment as develop
Used by the integration test CI job
"""
import pathlib
import sys

import spack.main
import spack.repo as sr
import spack.environment as senv


def main(repo_name):
    repo = sr.PATH.get_repo(repo_name)
    env = senv.active_environment()
    if not env:
        raise RuntimeError("requires active environment")
    develop = spack.main.SpackCommand("develop")
    for spec in env.user_specs:
        pkg_path = pathlib.Path(repo.package_path(spec.name))
        source_path = pkg_path.parent / f"{spec.name}-src"
        develop("-p", str(source_path), spec.name, capture=False)


if __name__ == "__main__":
    main(sys.argv[1])