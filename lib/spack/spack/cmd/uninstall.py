import spack.packages as packages

def setup_parser(subparser):
    subparser.add_argument('names', nargs='+', help="name(s) of package(s) to uninstall")
    subparser.add_argument('-f', '--force', action='store_true', dest='force',
                           help="Ignore installed packages that depend on this one and remove it anyway.")

def uninstall(args):
    # get packages to uninstall as a list.
    pkgs = [packages.get(name) for name in args.names]

    # Sort packages to be uninstalled by the number of installed dependents
    # This ensures we do things in the right order
    def num_installed_deps(pkg):
        return len(pkg.installed_dependents)
    pkgs.sort(key=num_installed_deps)

    # Uninstall packages in order now.
    for pkg in pkgs:
        pkg.do_uninstall()
