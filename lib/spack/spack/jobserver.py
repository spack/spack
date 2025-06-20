# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This module encapsulates make jobserver functionality.

If a jobserver is enabled, make jobs will be dyamically allocated
to package builds during the installation process.
"""

# import array
# import fcntl
import os
import shutil
import sys
import tempfile
# import termios
from enum import IntEnum
from typing import Dict, List, Optional, Tuple, Type

import spack.config


class JobserverType(IntEnum):
    """Possible jobserver states"""

    # Do not set up jobserver.
    NONE = 0
    # Set up FIFO implementation of jobserver.
    FIFO = 1


def package_type(pkg):
    if pkg.spec.satisfies("gmake") and pkg.spec["gmake"].satisfies("@4.4:"):
        return JobserverType.FIFO
    elif pkg.spec.satisfies("ninja") and pkg.spec["ninja"].satisfies("@1.13.0:"):
        return JobserverType.FIFO
    return JobserverType.NONE


class Jobserver:
    """Interface class for jobserver"""

    @staticmethod
    def determine_type(
        packages: List["spack.package_base.PackageBase"],
    ) -> Type["spack.jobserver.Jobserver"]:
        """Determine the type of jobserver to be used based on the packages
        required for the build."""
        js_types = [package_type(pkg) for pkg in packages]
        js_type = max(js_types)
        js_class = jobserver_class_table[js_type]
        return js_class

    def enable(self):
        """Enable the specified type of jobserver."""
        raise NotImplementedError("#TODO")

    def cleanup(self):
        """Clean up and close the specified type of jobserver."""
        raise NotImplementedError("TODO")

  #  # test if it's reading and writing bytes for fifo
  #  def get_available_bytes(self):
  #      """Gets the number of bytes available for reading from a file descriptor."""
  #      raise NotImplementedError("TODO")


class NoopJobserver(Jobserver):
    def enable(self):
        return None

    def cleanup(self):
        return None

  #  def get_available_bytes(self, fd):
  #      pass


class FifoJobserver(Jobserver):
    """Class for jobserver for builds that use Make version 4.4+ and
    Ninja version 1.13.0+ on non-Windows machines."""

    def __init__(self):
        self.fifo_directory = None
        self.fifo_read_fd = None
        self.fifo_write_fd = None

    def enable(self) -> Tuple[Optional[str], Optional[int]]:
        """Setup and enable FIFO implementation of make jobserver."""

        mflags = os.environ.get("MAKEFLAGS")
        if mflags and "--jobserver" in mflags:
            # jobserver already set up by make (through env depfile)
            return None, None

        if sys.platform != "win32":
            # create a named FIFO pipe for make jobserver
            self.fifo_directory = tempfile.mkdtemp(prefix="jobserver_fifo")
            fifo_path = os.path.join(self.fifo_directory, "jobserver")

            # create the FIFO
            os.mkfifo(fifo_path)

            # determine number of tokens for FIFO by -j value
            num_jobs = spack.config.determine_number_of_jobs(parallel=True)
            js_tokens = b"+" * num_jobs

            # open the FIFO for both reading and writing
            self.fifo_read_fd = os.open(fifo_path, os.O_RDONLY | os.O_NONBLOCK)
            self.fifo_write_fd = os.open(fifo_path, os.O_WRONLY | os.O_NONBLOCK)

            # initialize FIFO with job tokens
            os.write(self.fifo_write_fd, js_tokens)

            # set MAKEFLAGS environment variable for make jobserver
            os.environ["MAKEFLAGS"] = f"--jobserver-auth=fifo:{fifo_path} -j {num_jobs}"

            return self.fifo_directory, self.fifo_write_fd
        return None, None

    # TODO: Implement Windows support.

    def cleanup(self) -> None:
        """Clean up file descriptors and remove the FIFO directory used by them jobserver."""
        if self.fifo_read_fd is not None:
            os.close(self.fifo_read_fd)
        if self.fifo_write_fd is not None:
            os.close(self.fifo_write_fd)
        if self.fifo_directory is not None:
            shutil.rmtree(self.fifo_directory)

  #  def get_available_bytes(self):
  #      """Gets the number of bytes available for reading from a file descriptor."""
  #      bytes_available = array.array("i", [0])
  #      fcntl.ioctl(self.fifo_read_fd, termios.FIONREAD, bytes_available)
  #      return bytes_available[0]


# Table mapping JobserverType to Jobserver class
jobserver_class_table: Dict[JobserverType, Type[Jobserver]] = {
    JobserverType.NONE: NoopJobserver,
    JobserverType.FIFO: FifoJobserver,
}
