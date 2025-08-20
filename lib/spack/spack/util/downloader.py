# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import http.client
import os
import re
import sys
import time
import urllib.request
import warnings
from typing import Callable, List, Mapping, NamedTuple, Optional

import spack.llnl.util.filesystem as fs

from .executable import Executable
from .web import SPACK_USER_AGENT, base_curl_fetch_args, check_curl_code, require_curl, urlopen


class DownloadInfo(NamedTuple):
    """Information about a download."""

    url: str
    effective_url: str
    path: str
    headers: str


class Downloader:
    """Interface for downloading files."""

    def download_file(self, *, url, saved_file, timeout: Optional[int] = None) -> DownloadInfo:
        """Downloads a file from the specified URL and saves it to the given path.

        Args:
            url: the URL from which the file should be downloaded.
            saved_file: the local file path where the downloaded file will be saved.
            timeout: timeout in seconds for the download.

        Returns:
            DownloadInfo: An object containing details about the downloaded file,
            including the original URL, effective URL after redirects, saved path,
            and response headers.
        """
        raise NotImplementedError


class UrllibDownloader(Downloader):
    """Downloader that uses urllib."""

    def __init__(self, *, chunk_size=65536):
        self.chunk_size = chunk_size

    def download_file(
        self, *, url: str, saved_file: str, timeout: Optional[int] = None
    ) -> DownloadInfo:
        request = urllib.request.Request(url, headers={"User-Agent": SPACK_USER_AGENT})

        if os.path.lexists(saved_file):
            os.remove(saved_file)

        response = urlopen(request, timeout=timeout)
        progress = FetchProgress.from_headers(response.headers, enabled=sys.stdout.isatty())
        with open(saved_file, "wb") as f:
            while True:
                chunk = response.read(self.chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                progress.advance(len(chunk))
        progress.print(final=True)

        # Sometimes we're redirected to an arbitrary broken mirror, leading to spurious download
        # failures. In that case it's helpful for users to know which URL was actually fetched.
        effective_url = url
        if isinstance(response, http.client.HTTPResponse):
            effective_url = response.geturl()
        download_info = DownloadInfo(
            url=url, effective_url=effective_url, path=saved_file, headers=str(response.headers)
        )
        _check_headers(download_info)
        return download_info


class CurlDownloader(Downloader):
    """Downloader that uses curl."""

    _curl_exe: Optional[Executable] = None

    def __init__(
        self,
        *,
        config_args: Optional[List[str]] = None,
        cookie: Optional[str] = None,
        timeout: int = 0,
    ):
        self.cookie = cookie
        self.timeout = timeout
        self.config_args: List[str] = config_args or []

    @property
    def curl(self) -> Executable:
        if CurlDownloader._curl_exe is None:
            CurlDownloader._curl_exe = require_curl()
        return CurlDownloader._curl_exe

    def download_file(
        self, *, url: str, saved_file: str, timeout: Optional[int] = None
    ) -> DownloadInfo:
        saved_file_dir = os.path.dirname(saved_file)
        partial_file = saved_file + ".part"

        save_args = [
            "-C",
            "-",  # continue partial downloads
            "-o",
            partial_file,
        ]  # use a .part file

        timeout = 0
        cookie_args = []
        if self.cookie:
            cookie_args.append("-j")  # junk cookies
            cookie_args.append("-b")  # specify cookie
            cookie_args.append(self.cookie)

        base_args = base_curl_fetch_args(url, timeout)
        curl_args = self.config_args + save_args + base_args + cookie_args

        # Run curl but grab the mime type from the http headers
        curl = self.curl
        with fs.working_dir(saved_file_dir):
            headers = curl(*curl_args, output=str, fail_on_error=False)

        if curl.returncode != 0:
            if os.path.lexists(partial_file):
                os.remove(partial_file)
            check_curl_code(curl.returncode)

        download_info = DownloadInfo(url=url, effective_url=url, path=saved_file, headers=headers)
        _check_headers(download_info)
        fs.rename(partial_file, saved_file)
        return download_info


class FetchProgress:
    #: Characters to rotate in the spinner.
    spinner = ["|", "/", "-", "\\"]

    def __init__(
        self,
        total_bytes: Optional[int] = None,
        enabled: bool = True,
        get_time: Callable[[], float] = time.time,
    ) -> None:
        """Initialize a FetchProgress instance.
        Args:
            total_bytes: Total number of bytes to download, if known.
            enabled: Whether to print progress information.
            get_time: Function to get the current time."""
        #: Number of bytes downloaded so far.
        self.current_bytes = 0
        #: Delta time between progress prints
        self.delta = 0.1
        #: Whether to print progress information.
        self.enabled = enabled
        #: Function to get the current time.
        self.get_time = get_time
        #: Time of last progress print to limit output
        self.last_printed = 0.0
        #: Time of start of download
        self.start_time = get_time() if enabled else 0.0
        #: Total number of bytes to download, if known.
        self.total_bytes = total_bytes if total_bytes and total_bytes > 0 else 0
        #: Index of spinner character to print (used if total bytes is unknown)
        self.index = 0

    @classmethod
    def from_headers(
        cls,
        headers: Mapping[str, str],
        enabled: bool = True,
        get_time: Callable[[], float] = time.time,
    ) -> "FetchProgress":
        """Create a FetchProgress instance from HTTP headers."""
        # headers.get is case-insensitive if it's from a HTTPResponse object.
        content_length = headers.get("Content-Length")
        try:
            total_bytes = int(content_length) if content_length else None
        except ValueError:
            total_bytes = None
        return cls(total_bytes=total_bytes, enabled=enabled, get_time=get_time)

    def advance(self, num_bytes: int, out=sys.stdout) -> None:
        if not self.enabled:
            return
        self.current_bytes += num_bytes
        self.print(out=out)

    def print(self, final: bool = False, out=sys.stdout) -> None:
        if not self.enabled:
            return
        current_time = self.get_time()
        if self.last_printed + self.delta < current_time or final:
            self.last_printed = current_time
            # print a newline if this is the final update
            maybe_newline = "\n" if final else ""
            # if we know the total bytes, show a percentage, otherwise a spinner
            if self.total_bytes > 0:
                percentage = min(100 * self.current_bytes / self.total_bytes, 100.0)
                percent_or_spinner = f"[{percentage:3.0f}%] "
            else:
                # only show the spinner if we are not at 100%
                if final:
                    percent_or_spinner = "[100%] "
                else:
                    percent_or_spinner = f"[ {self.spinner[self.index]}  ] "
                self.index = (self.index + 1) % len(self.spinner)

            print(
                f"\r    {percent_or_spinner}{_format_bytes(self.current_bytes)} "
                f"@ {_format_speed(self.current_bytes, current_time - self.start_time)}"
                f"{maybe_newline}",
                end="",
                flush=True,
                file=out,
            )


def _check_headers(download_info: DownloadInfo) -> None:
    # Check if we somehow got an HTML file rather than the archive we
    # asked for.  We only look at the last content type, to handle
    # redirects properly.
    content_types = re.findall(
        r"Content-Type:[^\r\n]+", download_info.headers, flags=re.IGNORECASE
    )
    if content_types and "text/html" in content_types[-1]:
        msg = (
            f"The contents of {download_info.path or 'the archive'} fetched from "
            f"{download_info.url} looks like HTML. This can indicate a broken URL, "
            f"or an internet gateway issue."
        )
        if download_info.effective_url != download_info.url:
            msg += f" The URL redirected to {download_info.effective_url}."
        warnings.warn(msg)


def _format_speed(total_bytes: int, elapsed: float) -> str:
    """Return a human-readable average download speed string."""
    elapsed = 1 if elapsed <= 0 else elapsed  # avoid divide by zero
    speed = total_bytes / elapsed
    if speed >= 1e9:
        return f"{speed / 1e9:6.1f} GB/s"
    elif speed >= 1e6:
        return f"{speed / 1e6:6.1f} MB/s"
    elif speed >= 1e3:
        return f"{speed / 1e3:6.1f} KB/s"
    return f"{speed:6.1f}  B/s"


def _format_bytes(total_bytes: int) -> str:
    """Return a human-readable total bytes string."""
    if total_bytes >= 1e9:
        return f"{total_bytes / 1e9:7.2f} GB"
    elif total_bytes >= 1e6:
        return f"{total_bytes / 1e6:7.2f} MB"
    elif total_bytes >= 1e3:
        return f"{total_bytes / 1e3:7.2f} KB"
    return f"{total_bytes:7.2f}  B"
