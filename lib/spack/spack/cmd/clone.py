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

import llnl.util.tty as tty
import json

import spack
import spack.cmd


from spack.fetch_strategy import URLFetchStrategy
from spack.stage import Stage

description = "Build and install packages"

def setup_parser(subparser):
    subparser.add_argument(
        '--fetch', action='store_true', dest='fetch',
        help="Only fetch the remote package, don't install it")
    subparser.add_argument(
        '--url',  action='store', dest='url',
        help="Github URL from which to retrieve the package")



def getDescriptorURL(url):
    builtUrl = url
    return builtUrl.replace("github.com","api.github.com/repos").replace("www.","")

def getDownloadURL(url, filename, branch="master"):
    builtUrl = url
    return ((builtUrl.replace("www.github.com","raw.githubusercontent.com"))+"/"+branch+"/"+filename)
                    
def clone(parser, args):
    if not args.url:
        tty.die("Clone requires a github URL")
    # https://api.github.com/repos/DavidPoliakoff/spack
    descriptorURL = getDescriptorURL(args.url)
    repoStatusFetcher = URLFetchStrategy(url=descriptorURL)
    repoStatusDict = {}
    branchStatusDict = {}
    branchName = ""
    with Stage(repoStatusFetcher) as stage:
        repoStatusFetcher.fetch()
        descriptor = stage.path + "/" + descriptorURL.split("/")[-1]
        with open(descriptor,"r") as statusFile:
            repoStatusDict = json.load(statusFile)
            branchName = repoStatusDict["default_branch"]

    branchStatusFetcher = URLFetchStrategy(url=descriptorURL + '/branches/' + branchName)
    with Stage(branchStatusFetcher) as stage:
        branchStatusFetcher.fetch()
        descriptor = stage.path + "/" + branchName
        with open(descriptor,"r") as statusFile:
            branchStatusDict = json.load(statusFile)

    downloadURL = getDownloadURL(args.url,"package.py",branchName)
    print "DOWNLOADING" +downloadURL
    packageFetcher = URLFetchStrategy(url=downloadURL)

    from spack import repository, config
    roots = spack.config.get_config('repos', spack.cmd.default_list_scope)
    testRepo = repository.Repo(roots[0])

    with Stage(packageFetcher) as stage:
        packageFetcher.fetch()
        descriptor = stage.path + "/package.py"
        packageDir = descriptor
    tty.die("All tty's must die")
    #specs = spack.cmd.parse_specs(args.packages, concretize=True)
    #for spec in specs:
    #    package = spack.repo.get(spec)
    #    with spack.installed_db.write_transaction():
    #        package.do_install(
    #            keep_prefix=args.keep_prefix,
    #            keep_stage=args.keep_stage,
    #            ignore_deps=args.ignore_deps,
    #            make_jobs=args.jobs,
    #            verbose=args.verbose,
    #            fake=args.fake,
    #            explicit=True)
