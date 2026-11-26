# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import sys

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *

#: Creates the file ``ready`` in the prefix once it runs. On POSIX it first locks the file
#: ``lock`` there, which stays locked for as long as the process exists.
SCRIPT = """
import os, signal, sys, time
if sys.argv[2] == "True":
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
if os.name == "posix":
    import fcntl
    fd = os.open(os.path.join(sys.argv[1], "lock"), os.O_CREAT | os.O_WRONLY)
    fcntl.flock(fd, fcntl.LOCK_EX)
open(os.path.join(sys.argv[1], "ready"), "w").close()
time.sleep(600)
"""


class BlockingInstall(Package):
    """This package blocks in a child process of its install method, so that tests can interrupt
    a running build."""

    homepage = "http://www.example.com"
    has_code = False

    version("1.0")

    variant("ignore_sigterm", default=False, description="The child process ignores SIGTERM")

    def install(self, spec, prefix):
        mkdirp(prefix)
        python = Executable(sys.executable)
        python("-c", SCRIPT, prefix, str(spec.satisfies("+ignore_sigterm")))
