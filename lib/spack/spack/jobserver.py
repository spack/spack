# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This module encapsulates make jobserver functionality.

If a jobserver is enabled, make and/or ninja jobs will be dyamically allocated
to package builds during the installation process.
"""

import os
import shutil
import sys
import tempfile
from enum import IntEnum
from typing import Dict, List, Optional, Tuple, Type

import spack.config
import spack.llnl.util.tty as tty


class JobserverType(IntEnum):
    """Possible jobserver states"""

    # Leave jobserver behavior unchanged.
    NONE = 0
    # Set up FIFO implementation of jobserver.
    FIFO = 1
    # Do not set up jobserver if a package cannot support it.
    DISABLE = 2


def package_type(pkg) -> JobserverType:
    """Identify the appropriate jobserver type for packages in build."""
    if pkg.spec.satisfies("gmake@4.4:") or pkg.spec.satisfies("ninja@1.13.0:"):
        return JobserverType.FIFO
    elif pkg.spec.satisfies("gmake@:4.3") or pkg.spec.satisfies("ninja@:1.12"):
        return JobserverType.DISABLE
    return JobserverType.NONE


class Jobserver:
    """Interface class for jobserver"""

    @staticmethod
    def determine_type(
        packages: List["spack.package_base.PackageBase"],
    ) -> "spack.jobserver.Jobserver":
        """Determine the type of jobserver to be used based on the packages
        required for the build."""
        if not packages:
            return NoopJobserver()
        js_types = [package_type(pkg) for pkg in packages]
        js_type = max(js_types)
        if js_type == JobserverType.DISABLE:
            tty.debug(
                "FIFO-based jobserver has been disabled, the version of the build tool being used "
                "(pre-gmake@4.4 or pre-ninja@1.13.0) does not support it."
            )
        js_class = jobserver_class_table[js_type]
        return js_class()

    def enable(self) -> Optional[Tuple[Optional[str], Optional[int]]]:
        """Enable the specified type of jobserver."""
        raise NotImplementedError

    def cleanup(self) -> None:
        """Clean up and close the specified type of jobserver."""
        raise NotImplementedError


class NoopJobserver(Jobserver):
    """Class for jobserver builds that either does not change the functionality of
    how the jobserver is set up OR disables FIFO functionality of the jobserver."""

    def enable(self) -> None:
        return None

    def cleanup(self) -> None:
        return None


class FifoJobserver(Jobserver):
    """Class for jobserver for builds that use Make version 4.4+ and
    Ninja version 1.13.0+ on non-Windows machines."""

    def __init__(self):
        """Initialize FIFO jobserver attributes to None."""
        self.fifo_directory: Optional[str] = None
        self.fifo_path: Optional[str] = None
        self.fifo_read_fd: Optional[int] = None
        self.fifo_write_fd: Optional[int] = None

    def enable(self) -> Tuple[Optional[str], Optional[int]]:
        """Setup and enable FIFO implementation of make jobserver."""
        mflags = os.environ.get("MAKEFLAGS")
        if not (mflags and "--jobserver" in mflags) and sys.platform != "win32":
            # create a named FIFO pipe for make jobserver
            self.fifo_directory = tempfile.mkdtemp(prefix="jobserver_fifo")
            self.fifo_path = os.path.join(self.fifo_directory, "jobserver")

            # create the FIFO
            os.mkfifo(self.fifo_path)

            # determine number of tokens for FIFO by -j value
            self.num_jobs = spack.config.determine_number_of_jobs(parallel=True)
            js_tokens = b"+" * self.num_jobs

            # open the FIFO for both reading and writing
            self.fifo_read_fd = os.open(self.fifo_path, os.O_RDONLY | os.O_NONBLOCK)
            self.fifo_write_fd = os.open(self.fifo_path, os.O_WRONLY | os.O_NONBLOCK)

            # initialize FIFO with job tokens
            os.write(self.fifo_write_fd, js_tokens)

            # set MAKEFLAGS environment variable for make jobserver
            os.environ["MAKEFLAGS"] = f" -j{self.num_jobs} --jobserver-auth=fifo:{self.fifo_path}"

            tty.debug(
                f"Initialized FIFO-based jobserver at {self.fifo_path} with {self.num_jobs} jobs."
            )

            return self.fifo_directory, self.fifo_write_fd
        return None, None

    # TODO: Implement Windows support.

    def cleanup(self) -> None:
        """Clean up file descriptors, remove FIFO, and check for missing jobserver tokens."""
        # Check for missing jobserver tokens
        if self.fifo_read_fd is not None and self.fifo_write_fd is not None:
            try:
                # Count however many tokens were returned
                tokens_returned = 0
                try:
                    token_bytes = os.read(self.fifo_read_fd, 1024)
                except BlockingIOError:
                    token_bytes = b""

                while token_bytes:
                    tokens_returned += len(token_bytes)
                    try:
                        token_bytes = os.read(self.fifo_read_fd, 1024)
                    except BlockingIOError:
                        break

                if tokens_returned < self.num_jobs:
                    tty.warn(
                        f"spack jobserver internal: exiting with {tokens_returned} "
                        f"tokens instead of {self.num_jobs} "
                        f"(missing {self.num_jobs - tokens_returned} token(s)).\n\n"
                        "This usually means that one of the packages built during this "
                        "install did not properly release its parallel build tokens.\n"
                        "Parallelism may be reduced in subsequent builds. "
                        "If you can, please report the list of packages that were built "
                        "when this message appeared.\n\n"
                        "This warning is safe to ignore."
                    )
                else:
                    tty.debug(f"spack jobserver internal: all {self.num_jobs} tokens returned.")
            except Exception as e:
                tty.warn(f"Jobserver cleanup: error checking tokens: {e}")

        # Clean up file descriptors and remove the FIFO directory and flags used by jobserver.
        if self.fifo_read_fd is not None:
            os.close(self.fifo_read_fd)
        if self.fifo_write_fd is not None:
            os.close(self.fifo_write_fd)
        if self.fifo_directory is not None:
            shutil.rmtree(self.fifo_directory)
        os.environ.pop("MAKEFLAGS", None)


# Table mapping JobserverType to Jobserver class
jobserver_class_table: Dict[JobserverType, Type[Jobserver]] = {
    JobserverType.NONE: NoopJobserver,
    JobserverType.FIFO: FifoJobserver,
    JobserverType.DISABLE: NoopJobserver,
}
