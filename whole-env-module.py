import argparse
import os

import spack.environment as ev
import spack.environment.shell
from spack.util.environment import EnvironmentModifications


def main():
    # parser.add_argument('name', type=str, help="Your name")
    # parser.add_argument('--age', type=int, help="Your age", default=18)
    # parser.add_argument('--greet', action='store_true', help="Greet the user")
    parser = argparse.ArgumentParser(description="Generate sourcing script")
    parser.add_argument('path', type=str, help="Where to generate the file")
    parser.add_argument('--shell', type=str, help="Target shell", default=None)
    args = parser.parse_args()
    generate_module(args)


def generate_module(args):
    active_env = ev.active_environment()

    view = None
    if active_env.has_view(ev.default_view_name):
        view = ev.default_view_name

    env_mods = EnvironmentModifications()
    cmds = spack.environment.shell.activate_header(
        env=active_env, shell=args.shell, prompt=None, view=view
    )
    env_mods.extend(spack.environment.shell.activate(env=active_env, view=view))
    cmds += env_mods.shell_modifications(args.shell, explicit=True)

    if os.path.exists(args.path):
        raise Exception(f"Already exists {args.path}")
    with open(args.path, "w") as f:
        f.write(cmds)

if __name__ == "__main__":
    main()