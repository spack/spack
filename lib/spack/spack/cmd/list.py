import os
import re

import spack
import spack.packages as packages
from spack.version import ver
from spack.colify import colify
import spack.url as url
import spack.tty as tty


description ="List spack packages"

def setup_parser(subparser):
    subparser.add_argument('-v', '--versions', metavar="PACKAGE", dest='version_package',
                           help='List available versions of a package (experimental).')
    subparser.add_argument('-i', '--installed', action='store_true', dest='installed',
                           help='List installed packages for each platform along with versions.')


def list(parser, args):
    if args.installed:
        pkgs = packages.installed_packages()
        for sys_type in pkgs:
            print "%s:" % sys_type
            package_vers = []
            for pkg in pkgs[sys_type]:
                pv = [pkg.name + "@" + v for v in pkg.installed_versions]
                package_vers.extend(pv)
            colify(sorted(package_vers), indent=4)

    elif args.version_package:
        pkg = packages.get(args.version_package)

        try:
            # Run curl but grab the mime type from the http headers
            listing = spack.curl('-s', '-L', pkg.list_url, return_output=True)
            url_regex = os.path.basename(url.wildcard_version(pkg.url))
            strings = re.findall(url_regex, listing)

            versions = []
            wildcard = pkg.version.wildcard()
            for s in strings:
                match = re.search(wildcard, s)
                if match:
                    versions.append(ver(match.group(0)))

            colify(str(v) for v in reversed(sorted(set(versions))))

        except:
            tty.die("Listing versions for %s failed" % pkg.name,
                    "Listing versions is experimental.  You may need to add the list_url",
                    "attribute to the package to tell Spack where to look for versions.")
            raise

    else:
        colify(packages.all_package_names())
