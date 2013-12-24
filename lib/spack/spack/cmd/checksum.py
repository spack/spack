import os
import re
import argparse
import hashlib
from pprint import pprint
from subprocess import CalledProcessError

import spack.tty as tty
import spack.packages as packages
import spack.util.crypto
from spack.stage import Stage, FailedDownloadError
from spack.colify import colify
from spack.version import *

default_number_to_fetch = 10

description ="Checksum available versions of a package, print out checksums for addition to a package file."

def setup_parser(subparser):
    subparser.add_argument(
        'package', metavar='PACKAGE', help='Package to list versions for')
    subparser.add_argument(
        'versions', nargs=argparse.REMAINDER, help='Versions to generate checksums for')


def checksum(parser, args):
    # get the package we're going to generate checksums for
    pkg = packages.get(args.package)

    # If the user asked for specific versions, use those.
    versions = [ver(v) for v in args.versions]

    if not all(type(v) == Version for v in versions):
        tty.die("Cannot generate checksums for version lists or " +
                "version ranges.  Use unambiguous versions.")

    if not versions:
        versions = pkg.fetch_available_versions()
        if not versions:
            tty.die("Could not fetch any available versions for %s." % pkg.name)

    versions = list(reversed(versions))
    urls = [pkg.url_for_version(v) for v in versions]

    version_listings = ["%-10s%s" % (v,u) for v, u in zip(versions, urls)]
    tty.msg("Found %s versions to checksum." % len(urls),
            *version_listings)

    print
    while True:
        ans = raw_input("How many would you like to checksum? (default 10, 0 to abort) ")
        try:
            if not ans:
                to_download = default_number_to_fetch
            else:
                to_download = int(ans)
            break
        except ValueError:
            tty.msg("Please enter a valid number.")
            pass

    if not to_download:
        tty.msg("Aborted.")
        return
    else:
        urls = urls[:to_download]

    tty.msg("Downloading...")
    hashes = []
    for url, version in zip(urls, versions):
        stage = Stage(url)
        try:
            stage.fetch()
            hashes.append(spack.util.crypto.checksum(
                hashlib.md5, stage.archive_file))
        except FailedDownloadError, e:
            tty.msg("Failed to fetch %s" % url)
            continue

        finally:
            stage.destroy()

    dict_string = ["{"]
    for i, (v, h) in enumerate(zip(versions, hashes)):
        comma = "" if i == len(hashes) - 1 else ","
        dict_string.append("    '%s' : '%s'%s" % (str(v), str(h), comma))
    dict_string.append("}")
    tty.msg("Checksummed new versions of %s:" % pkg.name, *dict_string)
