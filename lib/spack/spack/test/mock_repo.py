##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os
import shutil

from llnl.util.filesystem import *

import spack
from spack.version import ver
from spack.stage import Stage
from spack.util.executable import which


#
# VCS Systems used by mock repo code.
#
git      = which('git',      required=True)
svn      = which('svn',      required=True)
svnadmin = which('svnadmin', required=True)
hg       = which('hg',       required=True)
tar      = which('tar',      required=True)


class MockRepo(object):
    def __init__(self, stage_name, repo_name):
        """This creates a stage where some archive/repo files can be staged
           for testing spack's fetch strategies."""
        # Stage where this repo has been created
        self.stage = Stage(stage_name)

        # Full path to the repo within the stage.
        self.path = join_path(self.stage.path, repo_name)
        mkdirp(self.path)


class MockArchive(MockRepo):
    """Creates a very simple archive directory with a configure script and a
       makefile that installs to a prefix.  Tars it up into an archive."""

    def __init__(self):
        repo_name = 'mock-archive-repo'
        super(MockArchive, self).__init__('mock-archive-stage', repo_name)

        with working_dir(self.path):
            configure = join_path(self.path, 'configure')

            with open(configure, 'w') as cfg_file:
                cfg_file.write(
                    "#!/bin/sh\n"
                    "prefix=$(echo $1 | sed 's/--prefix=//')\n"
                    "cat > Makefile <<EOF\n"
                    "all:\n"
                    "\techo Building...\n\n"
                    "install:\n"
                    "\tmkdir -p $prefix\n"
                    "\ttouch $prefix/dummy_file\n"
                    "EOF\n")
            os.chmod(configure, 0755)

        with working_dir(self.stage.path):
            archive_name = "%s.tar.gz" % repo_name
            tar('-czf', archive_name, repo_name)

        self.archive_path = join_path(self.stage.path, archive_name)
        self.url = 'file://' + self.archive_path


class MockVCSRepo(MockRepo):
    def __init__(self, stage_name, repo_name):
        """This creates a stage and a repo directory within the stage."""
        super(MockVCSRepo, self).__init__(stage_name, repo_name)

        # Name for rev0 & rev1 files in the repo to be
        self.r0_file = 'r0_file'
        self.r1_file = 'r1_file'


class MockGitRepo(MockVCSRepo):
    def __init__(self):
        super(MockGitRepo, self).__init__('mock-git-stage', 'mock-git-repo')

        with working_dir(self.path):
            git('init')

            # r0 is just the first commit
            touch(self.r0_file)
            git('add', self.r0_file)
            git('commit', '-m', 'mock-git-repo r0')

            self.branch      = 'test-branch'
            self.branch_file = 'branch_file'
            git('branch', self.branch)

            self.tag_branch = 'tag-branch'
            self.tag_file   = 'tag_file'
            git('branch', self.tag_branch)

            # Check out first branch
            git('checkout', self.branch)
            touch(self.branch_file)
            git('add', self.branch_file)
            git('commit', '-m' 'r1 test branch')

            # Check out a second branch and tag it
            git('checkout', self.tag_branch)
            touch(self.tag_file)
            git('add', self.tag_file)
            git('commit', '-m' 'tag test branch')

            self.tag = 'test-tag'
            git('tag', self.tag)

            git('checkout', 'master')

            # R1 test is the same as test for branch
            self.r1      = self.rev_hash(self.branch)
            self.r1_file = self.branch_file

            self.url = self.path

    def rev_hash(self, rev):
        return git('rev-parse', rev, return_output=True).strip()


class MockSvnRepo(MockVCSRepo):
    def __init__(self):
        super(MockSvnRepo, self).__init__('mock-svn-stage', 'mock-svn-repo')

        self.url = 'file://' + self.path

        with working_dir(self.stage.path):
            svnadmin('create', self.path)

            tmp_path = join_path(self.stage.path, 'tmp-path')
            mkdirp(tmp_path)
            with working_dir(tmp_path):
                touch(self.r0_file)

            svn('import', tmp_path, self.url, '-m', 'Initial import r0')

            shutil.rmtree(tmp_path)
            svn('checkout', self.url, tmp_path)
            with working_dir(tmp_path):
                touch(self.r1_file)
                svn('add', self.r1_file)
                svn('ci', '-m', 'second revision r1')

            shutil.rmtree(tmp_path)

            self.r0 = '1'
            self.r1 = '2'


class MockHgRepo(MockVCSRepo):
    def __init__(self):
        super(MockHgRepo, self).__init__('mock-hg-stage', 'mock-hg-repo')
        self.url = 'file://' + self.path

        with working_dir(self.path):
            hg('init')

            touch(self.r0_file)
            hg('add', self.r0_file)
            hg('commit', '-m', 'revision 0', '-u', 'test')
            self.r0 = self.get_rev()

            touch(self.r1_file)
            hg('add', self.r1_file)
            hg('commit', '-m' 'revision 1', '-u', 'test')
            self.r1 = self.get_rev()

    def get_rev(self):
        """Get current mercurial revision."""
        return hg('id', '-i', return_output=True).strip()
