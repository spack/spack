import argparse

import spack.cmd
import spack.tty as tty
import spack.packages as packages

description="Remove an installed package"

def setup_parser(subparser):
    subparser.add_argument(
        '-f', '--force', action='store_true', dest='force',
        help="Remove regardless of whether other packages depend on this one.")
    subparser.add_argument(
        'packages', nargs=argparse.REMAINDER, help="specs of packages to uninstall")


def uninstall(parser, args):
    if not args.packages:
        tty.die("uninstall requires at least one package argument.")

    specs = spack.cmd.parse_specs(args.packages)

    # For each spec provided, make sure it refers to only one package.
    # Fail and ask user to be unambiguous if it doesn't
    pkgs = []
    for spec in specs:
        matching_specs = packages.get_installed(spec)
        if len(matching_specs) > 1:
            tty.die("%s matches multiple packages.  Which one did you mean?"
                    % spec, *matching_specs)

        elif len(matching_specs) == 0:
            tty.die("%s does not match any installed packages." % spec)

        installed_spec = matching_specs[0]
        pkgs.append(packages.get(installed_spec))

    # Sort packages to be uninstalled by the number of installed dependents
    # This ensures we do things in the right order
    def num_installed_deps(pkg):
        return len(pkg.installed_dependents)
    pkgs.sort(key=num_installed_deps)

    # Uninstall packages in order now.
    for pkg in pkgs:
        pkg.do_uninstall()
