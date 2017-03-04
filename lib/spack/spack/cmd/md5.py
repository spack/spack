##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import argparse
import hashlib
import os
from urlparse import urlparse

import llnl.util.tty as tty
import spack.util.crypto
from spack.stage import Stage, FailedDownloadError

description = "calculate md5 checksums for files/urls"


def setup_parser(subparser):
    setup_parser.parser = subparser
    subparser.add_argument('files', nargs=argparse.REMAINDER,
                           help="files/urls to checksum")


def compute_md5_checksum(url):
    if not os.path.isfile(url):
        with Stage(url) as stage:
            stage.fetch()
            value = spack.util.crypto.checksum(hashlib.md5, stage.archive_file)
    else:
        value = spack.util.crypto.checksum(hashlib.md5, url)
    return value


def normalized(files):
    for p in files:
        result = urlparse(p)
        value = p
        if not result.scheme:
            value = os.path.abspath(p)
        yield value


def md5(parser, args):
    if not args.files:
        setup_parser.parser.print_help()
        return 1

    urls = [x for x in normalized(args.files)]
    results = []
    for url in urls:
        try:
            checksum = compute_md5_checksum(url)
            results.append((checksum, url))
        except FailedDownloadError as e:
            tty.warn("Failed to fetch %s" % url)
            tty.warn("%s" % e)
        except IOError as e:
            tty.warn("Error when reading %s" % url)
            tty.warn("%s" % e)

    # Dump the MD5s at last without interleaving them with downloads
    checksum = 'checksum' if len(results) == 1 else 'checksums'
    tty.msg("%d MD5 %s:" % (len(results), checksum))
    for checksum, url in results:
        print("{0}  {1}".format(checksum, url))
