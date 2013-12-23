import re
import textwrap

import spack
import spack.packages as packages
from spack.colify import colify

description = "Get detailed information on a particular package"

def setup_parser(subparser):
    subparser.add_argument('name', metavar="PACKAGE", help="name of packages to get info on")


def info(parser, args):
    package = packages.get(args.name)
    print "Package:   ", package.name
    print "Homepage:  ", package.homepage
    print "Download:  ", package.url

    print
    print "Safe versions:  "

    if package.versions:
        colify(reversed(sorted(package.versions)), indent=4)
    else:
        print "None.  Use spack versions %s to get a list of downloadable versions." % package.name

    print
    print "Dependencies:"
    if package.dependencies:
        colify(package.dependencies, indent=4)
    else:
        print "    None"

    print
    print "Virtual packages: "
    if package.provided:
        for spec, when in package.provided.items():
            print "    %s provides %s" % (when, spec)
    else:
        print "    None"

    print
    print "Description:"
    if package.__doc__:
        doc = re.sub(r'\s+', ' ', package.__doc__)
        lines = textwrap.wrap(doc, 72)
        for line in lines:
            print "    " + line
    else:
        print "    None"
