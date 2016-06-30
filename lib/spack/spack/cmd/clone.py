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
import shutil
import os

import llnl.util.tty as tty

import spack
import spack.cmd


from spack.fetch_strategy import GitFetchStrategy
from spack.stage import Stage
from llnl.util.filesystem import join_path
from spack.repository import create_repo, canonicalize_path, BadRepoError, Repo

description = "Build and install packages"


def setup_parser(subparser):
    subparser.add_argument(
        '--url',  action='store', dest='url',
        help="Github URL from which to retrieve the package")

def getSpackGitRepo():
    def repo_add_if_not_exists(path, scope=spack.cmd.default_list_scope):
        """Add a package source to Spack's configuration."""

        # real_path is absolute and handles substitution.
        canon_path = canonicalize_path(path)

        # check if the path exists
        if not os.path.exists(canon_path):
            tty.die("No such file or directory: %s" % path)

        # Make sure the path is a directory.
        if not os.path.isdir(canon_path):
            tty.die("Not a Spack repository: %s" % path)

        # Make sure it's actually a spack repository by constructing it.
        repo = Repo(canon_path)

        # If that succeeds, finally add it to the configuration.
        repos = spack.config.get_config('repos', scope)
        if not repos:
            repos = []

        if repo.root in repos or path in repos:
            return

        repos.insert(0, canon_path)
        spack.config.update_config('repos', repos, scope)
        tty.msg("Created repo with namespace '%s'." % repo.namespace)
    spack_git_repo_path = join_path(spack.repos_path, "git")
    try:
        create_repo(spack_git_repo_path, "git")
    except BadRepoError:
        pass
    repo_add_if_not_exists(spack_git_repo_path)
    git_repo = Repo(spack_git_repo_path)
    return git_repo

def integrate_github_package(url):
    repoFetcher = GitFetchStrategy(git=url)
    packageName = url.split("/")[-1]
    git_repo = getSpackGitRepo()
    spack_git_repo_path = git_repo.packages_path
    packageDest = join_path(spack_git_repo_path, packageName)
    if not os.path.isdir(packageDest):
        os.mkdir(packageDest)
    with Stage(repoFetcher) as stage:
        repoFetcher.fetch()
        packagePath = stage.path + "/" + packageName + "/package.py"
        shutil.copy2(packagePath, packageDest)
    return packageName

def clone(parser,args):
    if not args.url:
        tty.die("Clone requires a github URL")
    packageName = integrate_github_package(args.url)
    specs = spack.cmd.parse_specs(packageName, concretize=True)
    git_repo = getSpackGitRepo()
    for spec in specs:
        package = git_repo.get(spec)
        with spack.installed_db.write_transaction():
            package.do_install(explicit=True)
