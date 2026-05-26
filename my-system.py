# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import argparse
import json
import os
import pathlib
import shutil

from llnl.util.filesystem import mkdirp

import spack.vendor.archspec.cpu
import spack.vendor.archspec.cpu.platform

import spack.config as config
import spack.database
import spack.environment as ev
import spack.llnl.util.tty as tty
import spack.platforms
import spack.repo
import spack.solver.asp  # noqa: F401
import spack.solver.reuse
import spack.store
import spack.util.spack_yaml as syaml


def _dump_section(section, stream):
    data = syaml.syaml_dict()
    data[section] = config.CONFIG.get_config(section, scope=None)
    syaml.dump_config(data, stream=stream, default_flow_style=False, blame=False)


def _represent_platform_as_json(dst):
    import spack.compilers.config
    import spack.compilers.libraries as cmp_lib
    import spack.config

    cmp_cache = cmp_lib.CompilerCache()

    compiler_save_libc = dict()
    if spack.solver.asp.using_libc_compatibility():
        for cmp in spack.compilers.config.all_compilers_from(spack.config.CONFIG):
            cmp_cache.get(cmp).c_compiler_output
            compiler_save_libc[cmp.format("{name}@{version}")] = cmp_lib.CompilerPropertyDetector(
                cmp
            ).default_libc()

    # Convert objects to JSON-serializable data
    platform_obj = spack.platforms.host()
    cpu_obj = spack.vendor.archspec.cpu.host()

    # Capture OS information using the new to_json method
    platform_data = platform_obj.to_json()

    # Serialize libcs (convert Spec objects to strings)
    all_libcs_specs = spack.solver.asp.all_libcs()
    all_libcs_str = [str(spec) for spec in all_libcs_specs]

    # Serialize compiler libcs (convert Spec objects to strings)
    compiler_libc_str = {
        key: str(value) if value else None for key, value in compiler_save_libc.items()
    }

    data = {
        "platform_machine": spack.vendor.archspec.cpu.platform.machine(),
        "platform_class": platform_obj.__class__.__name__,
        "platform_data": platform_data,
        "cpu_target": str(cpu_obj),
        "all_libcs": all_libcs_str,
        "compiler_libc": compiler_libc_str,
        "using_libc_compat": int(spack.solver.asp.using_libc_compatibility()),
    }

    with open(dst, "w") as f:
        json.dump(data, f, indent=2)


def _simulate_system(state_dir):
    import sys

    import spack.vendor.archspec.cpu.microarchitecture

    import spack.compilers.libraries

    with open(os.path.join(state_dir, "arch.json"), "r") as f:
        data = json.load(f)

        # If a package.py file does "import sys", this will change the value
        # of sys.platform in that context
        platform_to_sys_platform = {
            "Linux": "linux",
            "Darwin": "darwin",
            "Windows": "win32",
            "FreeBSD": "freebsd",
        }
        spack.repo._spack_simulated_platform = platform_to_sys_platform.get(
            data["platform_class"], data["platform_class"].lower()
        )
        spack.repo._spack_simulated_machine = data["platform_machine"]

        # Clear any cached package modules so they'll be re-imported with patched values
        pkg_modules = [
            key
            for key in list(sys.modules.keys())
            if key.startswith("spack.pkg.")
            or (key.startswith("spack_repo.") and ".packages." in key)
        ]
        for key in pkg_modules:
            del sys.modules[key]

        # Also clear importlib caches to ensure modules are truly reloaded
        import importlib

        importlib.invalidate_caches()

        # Clear the virtual provider index (provider availability can differ by platform)
        if hasattr(spack.repo.PATH, "_provider_index"):
            spack.repo.PATH._provider_index = None

        # Also clear the on-disk provider cache files
        # Provider index is cached at: cache/providers/<namespace>-specfile_v<version>-index.json
        for repo in spack.repo.PATH.repos:
            if hasattr(repo, "_repo_index") and repo._repo_index is not None:
                # Force rebuild of provider index by clearing the cache
                repo._repo_index = None

            # Delete the on-disk provider cache files
            if hasattr(repo, "_cache") and repo._cache is not None:
                import glob

                provider_cache_pattern = os.path.join(
                    repo._cache.root, "providers", f"{repo.namespace}-*.json"
                )
                for cache_file in glob.glob(provider_cache_pattern):
                    try:
                        os.remove(cache_file)
                    except Exception:
                        pass  # Ignore errors deleting cache files

        # Restore platform using the new from_json method
        spack.vendor.archspec.cpu.platform._machine_override = data["platform_machine"]
        spack.vendor.archspec.cpu.microarchitecture.module_reinitialize()

        # Create platform object using from_json (avoids platform-specific initialization)
        platform_cls = getattr(spack.platforms, data["platform_class"])
        simulated_platform = platform_cls.from_json(data["platform_data"])

        # Override spack.platforms.host() to return simulated platform
        spack.platforms.host = lambda: simulated_platform

        # Restore CPU - reconstruct from string
        cpu_target_name = data["cpu_target"]
        simulated_cpu = spack.vendor.archspec.cpu.TARGETS[cpu_target_name]
        spack.vendor.archspec.cpu.host = lambda: simulated_cpu

        # Restore libcs (convert strings back to Spec objects)
        import spack.spec

        all_libcs_specs = {spack.spec.Spec(s) for s in data["all_libcs"]}
        spack.solver.asp.all_libcs = lambda: all_libcs_specs
        spack.solver.asp.c_compiler_runs = lambda x: True

        # Restore compiler libc mapping (convert strings back to Spec objects)
        compiler_libc_specs = {
            key: spack.spec.Spec(value) if value else None
            for key, value in data["compiler_libc"].items()
        }
        spack.compilers.libraries.CompilerPropertyDetector._simulated_libc = compiler_libc_specs

        # Restore libc compatibility flag
        spack.solver.asp.using_libc_compatibility = lambda: bool(data["using_libc_compat"])

        reuse_db = spack.database.Database(str(pathlib.Path(state_dir) / "reuse"))
        spack.solver.reuse._simulate_reusable = reuse_db.query()


def _make_env(dst_dir):
    user_specs = []

    env = ev.active_environment()
    if env:
        with env:
            user_specs = env.user_specs.specs_as_yaml_list

    entries = {}
    for repo in spack.repo.PATH.repos:
        # copy each repo location recursively into the dst_dir
        # Generate new repos: config with $env-relative paths
        name = repo.namespace
        path = repo.root
        mkdirp(os.path.join(dst_dir, "repos", "spack_repo"))
        shutil.copytree(path, os.path.join(dst_dir, "repos", "spack_repo", name))
        entries[name] = f"$env/repos/spack_repo/{name}"

    env_yaml = {
        "spack": {
            "specs": user_specs,
            "view": False,
            "config": {"install_tree:": {"root": "$env/database"}},
            "packages:": config.get("packages"),
            "concretizer:": config.get("concretizer"),
            "repos:": entries,
        }
    }
    with open(os.path.join(dst_dir, "spack.yaml"), mode="wb") as f:
        syaml.dump_config(env_yaml, stream=f, default_flow_style=False, blame=False)


def generate(args):
    if os.path.exists(args.dest):
        raise ValueError(f"Dest already exists: {args.dest}")

    root = pathlib.Path(args.dest)
    cfg = root / "config"
    mkdirp(cfg)
    with open(cfg / "packages.yaml", "w") as f:
        _dump_section("packages", f)
    with open(cfg / "concretizer.yaml", "w") as f:
        _dump_section("concretizer", f)

    tty.debug(f"[simulate] Make env {root}")
    _make_env(root)
    tty.debug("[simulate] Serializing in-memory platform state to JSON")
    _represent_platform_as_json(root / "arch.json")

    # Copy the database of installed specs
    # (doesn't account for upstreams)
    tty.debug("[simulate] Saving local DB")
    db = spack.store.STORE.db
    rel_index_path = pathlib.Path(db._index_path).relative_to(db.root)
    env_db_root = pathlib.Path(root) / "database"
    env_db_index = env_db_root / rel_index_path
    mkdirp(env_db_index.parents[0])
    if os.path.exists(db._index_path):
        shutil.copy(db._index_path, env_db_index)

    tty.debug("[simulate] Collect all reusable specs")
    solver = spack.solver.asp.Solver()
    reusable_specs = solver.selector.reusable_specs([])
    reuse_db_root = pathlib.Path(root) / "reuse"
    reuse_db = spack.database.Database(str(reuse_db_root))
    with reuse_db.write_transaction():
        for spec in reusable_specs:
            reuse_db._add(spec)


def use(args):
    import spack.bootstrap as bootstrap
    import spack.main

    with bootstrap.ensure_bootstrap_configuration():
        bootstrap.ensure_clingo_importable_or_raise()

    _simulate_system(args.source)
    e = ev.Environment(args.source)
    with e:
        spack.main.SpackCommand(args.command[0])(*args.command[1:], capture=False)


def main():
    parser = argparse.ArgumentParser(description="For simulating other systems/configs")

    sp = parser.add_subparsers(metavar="SUBCOMMAND", dest="simulate_command")

    gen_parser = sp.add_parser(
        "generate", help="Put all simulation resources in this dir (for target system to use)"
    )
    gen_parser.add_argument(
        "dest", help="Put all simulation resources in this dir (for target system to use)"
    )

    use_parser = sp.add_parser("use", help="Use a generated system")
    use_parser.add_argument("source", help="Directory generated by `my-system.py generate`")
    use_parser.add_argument("command", nargs=argparse.REMAINDER, help="command to run")

    args = parser.parse_args()

    action = {"generate": generate, "use": use}
    action[args.simulate_command](args)


if __name__ == "__main__":
    main()
