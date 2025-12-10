# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import io
import os
import shlex
import tempfile
import urllib.parse
import warnings
from pathlib import Path

import spack.error
import spack.stage
from spack.llnl.util import tty
from spack.util.executable import which


class SSHConnection(object):
    # used to cache connection objects and avoid checking SSH config multiple times
    _connections: dict[str, "SSHConnection"] = {}

    @classmethod
    def from_url(cls, url):
        if isinstance(url, str):
            url = urllib.parse.urlparse(url)
        if url.netloc not in cls._connections:
            cls._connections[url.netloc] = SSHConnection(url.netloc)
        return cls._connections[url.netloc]

    def __init__(self, netloc):
        SSH_DEFAULT_ARGS = [] if tty.is_debug() else ["-q", "-o", "LogLevel=QUIET"]
        self.ssh = which("ssh", required=True).with_default_args(*SSH_DEFAULT_ARGS)
        self.scp = which("scp", required=True).with_default_args(*SSH_DEFAULT_ARGS)
        self.netloc = netloc

        has_control_master = False
        for config_line in self.ssh("-G", netloc, fail_on_error=True, output=str).splitlines():
            if config_line == "controlmaster true" or config_line == "controlmaster auto":
                has_control_master = True
                break

        if not has_control_master:
            warnings.warn(
                f"Minimize SSH connections to {netloc} via 'ControlMaster' in your SSH config!"
            )

    def exists(self, path):
        self.ssh(self.netloc, f"test -e {shlex.quote(path)}", fail_on_error=False)
        return self.ssh.returncode == 0

    def list_path(self, path, recursive=False):
        if recursive:
            output = self.ssh(self.netloc, f"find {shlex.quote(path)} -type f", output=str)
        else:
            output = self.ssh(
                self.netloc, f"find {shlex.quote(path)} -maxdepth 1 -type f", output=str
            )
        return (
            [str(Path(p.strip()).relative_to(path)) for p in output.splitlines()] if output else []
        )

    def stat_path(self, path):
        output = (
            self.ssh(
                self.netloc,
                f'stat -c "%s %Y" {shlex.quote(path)} 2>/dev/null || '  # Linux
                f'stat -f "%z %m" {shlex.quote(path)} 2>/dev/null',  # MacOS / BSD
                output=str,
            )
            .strip()
            .split()
        )
        if self.ssh.returncode != 0:
            return None
        size = int(output[0])
        mtime = float(output[1])
        return size, mtime

    def fetch(self, remote_path, dest):
        self.scp(shlex.quote(f"{self.netloc}:{remote_path}"), dest, fail_on_error=True)

    def read(self, remote_path):
        with tempfile.NamedTemporaryFile("rb", dir=spack.stage.get_stage_root()) as tmp:
            try:
                self.fetch(remote_path, tmp.name)
                return io.BytesIO(tmp.read())
            except Exception as e:
                raise SpackSSHError(
                    f"Download of ssh://{self.netloc}:{remote_path} failed: {e.__class__.__name__}: {e}"
                )

    def push(self, local_path, remote_path, keep_original=True):
        self.ssh(
            self.netloc,
            f"mkdir -p {shlex.quote(os.path.dirname(remote_path))}",
            fail_on_error=True,
        )
        self.scp(local_path, shlex.quote(f"{self.netloc}:{remote_path}"), fail_on_error=True)
        if not keep_original:
            os.remove(local_path)


class SpackSSHError(spack.error.SpackError):
    """Superclass for Spack SSH errors."""
