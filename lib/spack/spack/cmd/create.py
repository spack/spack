import string
import os
import hashlib
import re

import spack
import spack.packages as packages
import spack.tty as tty
import spack.url
import spack.util.crypto as crypto

from spack.util.executable import which
from spack.stage import Stage
from contextlib import closing

description = "Create a new package file from an archive URL"

package_template = string.Template("""\
# FIXME:
# This is a template package file for Spack.  We've conveniently
# put giant "FIXME" labels next to all the things you'll probably
# want to change.
#
# Once you've edited all the FIXME's, delete this whole message,
# save this file, and test out your package like this:
#
#     spack install ${name}
#
# You can always get back here with 'spack edit ${name}'.  See
# the spack documentation for more information on building
# packages.
#
from spack import *

class ${class_name}(Package):
    ""\"FIXME: put a proper description of your package here.""\"
    # FIXME: add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "${url}"

    versions = ${versions}

    def install(self, prefix):
        # FIXME: Modify the configure line to suit your build system here.
        ${configure}

        # FIXME:
        make()
        make("install")
""")


def setup_parser(subparser):
    subparser.add_argument('url', nargs='?', help="url of package archive")
    subparser.add_argument('-f', '--force', action='store_true', dest='force',
                           help="Remove existing package file.")


def guess_configure(archive_file):
    """Try to guess the type of build system used by the project, and return
       an appropriate configure line.
    """
    tar = which('tar')
    output = tar("--exclude=*/*/*", "-tf", archive_file, return_output=True)

    autotools = 'configure("--prefix=%s" % prefix)'
    cmake     = 'cmake(".", *std_cmake_args)'
    lines = output.split('\n')

    if any(re.search(r'/configure$', l) for l in lines):
        return autotools
    elif  any(re.search(r'/CMakeLists.txt$', l) for l in lines):
        return cmake
    else:
        # Both, with cmake commented out
        return '%s\n        # %s' % (autotools, cmake)


def create(parser, args):
    url = args.url

    # Try to deduce name and version of the new package from the URL
    name, version = spack.url.parse_name_and_version(url)
    if not name:
        print "Couldn't guess a name for this package."
        while not name:
            new_name = raw_input("Name: ")
            if packages.valid_name(name):
                name = new_name
            else:
                print "Package names must contain letters, numbers, and '_' or '-'"

    if not version:
        tty.die("Couldn't guess a version string from %s." % url)

    path = packages.filename_for_package_name(name)
    if not args.force and os.path.exists(path):
        tty.die("%s already exists." % path)

    # make a stage and fetch the archive.
    try:
        stage = Stage(url)
        archive_file = stage.fetch()
    except spack.FailedDownloadException, e:
        tty.die(e.message)

    md5 = crypto.checksum(hashlib.md5, archive_file)
    versions = '{ "%s" : "%s" }' % (version, md5)
    class_name = packages.class_name_for_package_name(name)
    configure = guess_configure(archive_file)

    # Write out a template for the file
    tty.msg("Editing %s." % path)
    with closing(open(path, "w")) as pkg_file:
        pkg_file.write(
            package_template.substitute(
                name=name,
                configure=configure,
                class_name=class_name,
                url=url,
                versions=versions))

    # If everything checks out, go ahead and edit.
    spack.editor(path)
