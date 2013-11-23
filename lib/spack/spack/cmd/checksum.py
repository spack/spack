import os
import re
import argparse
from pprint import pprint
from subprocess import CalledProcessError

import spack.tty as tty
import spack.packages as packages
from spack.stage import Stage
from spack.colify import colify
from spack.util.crypto import md5
from spack.version import *

group='foo'
description ="Checksum available versions of a package, print out checksums for addition to a package file."

def setup_parser(subparser):
    subparser.add_argument('package', metavar='PACKAGE', help='Package to list versions for')
    subparser.add_argument('versions', nargs=argparse.REMAINDER, help='Versions to generate checksums for')
    subparser.add_argument('-n', '--number', dest='number', type=int,
                           default=10, help='Number of versions to list')


def checksum(parser, args):
    # get the package we're going to generate checksums for
    pkg = packages.get(args.package)

    # If the user asked for specific versions, use those.
    # Otherwise get the latest n, where n is from the -n/--number param
    versions = [ver(v) for v in args.versions]

    if not all(type(v) == Version for v in versions):
        tty.die("Cannot generate checksums for version lists or " +
                "version ranges.  Use unambiguous versions.")

    if not versions:
        versions = pkg.fetch_available_versions()[:args.number]
        if not versions:
            tty.die("Could not fetch any available versions for %s."
                    % pkg.name)

    versions.sort()
    versions.reverse()
    urls = [pkg.url_for_version(v) for v in versions]

    tty.msg("Found %s versions to checksum." % len(urls))
    tty.msg("Downloading...")

    hashes = []
    for url, version in zip(urls, versions):
        stage = Stage("checksum-%s-%s" % (pkg.name, version), url)
        try:
            stage.fetch()
            hashes.append(md5(stage.archive_file))
        finally:
            stage.destroy()

    dict_string = ["{"]
    for i, (v, h) in enumerate(zip(versions, hashes)):
        comma = "" if i == len(hashes) - 1 else ","
        dict_string.append("    '%s' : '%s'%s" % (str(v), str(h), comma))
    dict_string.append("}")
    tty.msg("Checksummed new versions of %s:" % pkg.name, *dict_string)
