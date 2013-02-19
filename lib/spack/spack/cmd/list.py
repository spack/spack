import spack
import spack.packages as packages
from spack.colify import colify


def setup_parser(subparser):
    subparser.add_argument('-i', '--installed', action='store_true', dest='installed',
                           help='List installed packages for each platform along with versions.')


def list(args):
    if args.installed:
        pkgs = packages.installed_packages()
        for sys_type in pkgs:
            print "%s:" % sys_type
            package_vers = []
            for pkg in pkgs[sys_type]:
                pv = [pkg.name + "/" + v for v in pkg.installed_versions]
                package_vers.extend(pv)
            colify(sorted(package_vers), indent=4)
    else:
        colify(packages.all_package_names())
