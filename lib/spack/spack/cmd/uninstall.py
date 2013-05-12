import spack.cmd
import spack.packages as packages
import argparse

description="Remove an installed package"

def setup_parser(subparser):
    subparser.add_argument('-f', '--force', action='store_true', dest='force',
                           help="Ignore installed packages that depend on this one and remove it anyway.")
    subparser.add_argument('packages', nargs=argparse.REMAINDER, help="specs of packages to uninstall")

def uninstall(parser, args):
    if not args.packages:
        tty.die("uninstall requires at least one package argument.")

    specs = spack.cmd.parse_specs(args.packages)

    # get packages to uninstall as a list.
    pkgs = [packages.get(spec.name) for spec in specs]

    # Sort packages to be uninstalled by the number of installed dependents
    # This ensures we do things in the right order
    def num_installed_deps(pkg):
        return len(pkg.installed_dependents)
    pkgs.sort(key=num_installed_deps)

    # Uninstall packages in order now.
    for pkg in pkgs:
        pkg.do_uninstall()
