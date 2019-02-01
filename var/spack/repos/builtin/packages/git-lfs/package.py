# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GitLfs(MakefilePackage):
    """Git LFS is a system for managing and versioning large files in
       association with a Git repository.  Instead of storing the large files
       within the Git repository as blobs, Git LFS stores special "pointer
       files" in the repository, while storing the actual file contents on a
       Git LFS server."""

    homepage = "https://git-lfs.github.com"
    url      = "https://github.com/git-lfs/git-lfs/archive/v2.6.1.tar.gz"

    version('2.6.1', sha256='e17cd9d4e66d1116be32f7ddc7e660c7f8fabbf510bc01b01ec15a22dd934ead')

    depends_on('go@1.5:', type='build')
    depends_on('git@1.8.2:', type='run')

    parallel = False

    # Git-lfs does not provide an 'install' target in the Makefile
    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install(join_path('bin', 'git-lfs'), prefix.bin)
