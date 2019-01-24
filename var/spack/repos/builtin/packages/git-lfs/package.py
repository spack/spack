# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GitLfs(Package):
    """Git LFS is a system for managing and versioning large files in
       association with a Git repository.  Instead of storing the large files
       within the Git repository as blobs, Git LFS stores special "pointer
       files" in the repository, while storing the actual file contents on a
       Git LFS server."""

    homepage = "https://git-lfs.github.com"
    git      = "https://github.com/github/git-lfs.git"

    version('2.3.0', tag='v2.3.0')
    version('2.2.1', tag='v2.2.1')
    version('2.0.2', tag='v2.0.2')
    version('1.4.1', tag='v1.4.1')
    version('1.3.1', tag='v1.3.1')

    # TODO: Add tests by following the instructions at this location:
    # https://github.com/github/git-lfs/blob/master/CONTRIBUTING.md#building

    depends_on('go@1.5:', type='build')
    depends_on('git@1.8.2:', type='run')

    def install(self, spec, prefix):
        bootstrap_script = Executable(join_path('script', 'bootstrap'))
        bootstrap_script()

        mkdirp(prefix.bin)
        install(join_path('bin', 'git-lfs'), prefix.bin)
