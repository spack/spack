# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import http.client
import subprocess
import sys
import time
import urllib.request
import warnings
from typing import Callable, List, NamedTuple, Optional, Tuple

import spack.llnl.util.filesystem as fs

from .executable import which_string
from .web import SPACK_USER_AGENT, base_curl_fetch_args, check_curl_code, urlopen


class DownloadInfo(NamedTuple):
    """Information about a download."""

    url: str
    effective_url: str
    path: str
    headers: http.client.HTTPMessage


class Downloader:
    """Interface for downloading files."""

    def __init__(self, *, chunk_size=65536):
        self.chunk_size = chunk_size

    def download_file(self, *, url: str, saved_file: str, timeout: int = 0) -> DownloadInfo:
        """Downloads a file from the specified URL and saves it to the given path.

        Args:
            url: the URL from which the file should be downloaded.
            saved_file: the local file path where the downloaded file will be saved.
            timeout: timeout in seconds for the download.

        Returns:
            An object containing details about the downloaded file,
            including the original URL, effective URL after redirects, saved path,
            and response headers.
        """
        # Sometimes we're redirected to an arbitrary broken mirror, leading to spurious download
        # failures. In that case it's helpful for users to know which URL was actually fetched.
        headers, effective_url = self._get_headers_and_effective_url(url, timeout=timeout)
        partial_file = saved_file + ".part"

        progress = FetchProgress.from_headers(headers, enabled=sys.stdout.isatty())
        self._start_body_read()
        with open(partial_file, "wb") as f:
            while True:
                chunk = self._read_body_chunk(size=self.chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                progress.advance(len(chunk))
        progress.print(final=True)
        self._finalize_body_read()

        fs.rename(partial_file, saved_file)
        download_info = DownloadInfo(
            url=url, effective_url=effective_url, path=saved_file, headers=headers
        )
        _check_headers(download_info)
        return download_info

    def _get_headers_and_effective_url(
        self, url: str, *, timeout: int
    ) -> Tuple[http.client.HTTPMessage, str]:
        """Returns headers and effective URL for a given URL."""
        raise NotImplementedError

    def _read_body_chunk(self, size: int) -> bytes:
        """Reads a chunk of the response body."""
        raise NotImplementedError

    def _finalize_body_read(self) -> None:
        """Finalizes reading the response body."""
        pass

    def _start_body_read(self) -> None:
        """Starts reading the response body."""
        pass


class UrllibDownloader(Downloader):
    """Downloader that uses urllib."""

    response: Optional[http.client.HTTPResponse] = None

    def _get_headers_and_effective_url(
        self, url: str, *, timeout: int
    ) -> Tuple[http.client.HTTPMessage, str]:
        request = urllib.request.Request(url, headers={"User-Agent": SPACK_USER_AGENT})
        self.response = urlopen(request, timeout=timeout)
        effective_url = url
        if isinstance(self.response, http.client.HTTPResponse):
            effective_url = self.response.geturl()
        return self.response.headers, effective_url

    def _read_body_chunk(self, size: int) -> bytes:
        assert self.response is not None, "response not set before calling _read_body_chunk"
        return self.response.read(size)


class CurlDownloader(Downloader):
    """Downloader that uses curl."""

    _curl_exe: Optional[str] = None
    _url: str = ""
    _timeout: int = 0
    _body_process: Optional[subprocess.Popen] = None

    def __init__(
        self,
        *,
        config_args: Optional[List[str]] = None,
        cookie: Optional[str] = None,
        chunk_size: int = 65536,
    ):
        super().__init__(chunk_size=chunk_size)
        self.cookie = cookie
        self.config_args: List[str] = config_args or []

    def _get_headers_and_effective_url(
        self, url: str, *, timeout: int
    ) -> Tuple[http.client.HTTPMessage, str]:
        self._url, self._timeout = url, timeout

        base_args = base_curl_fetch_args(
            self._url, self._timeout, headers=False, status_bar=False, user_agent=SPACK_USER_AGENT
        )
        header_args = ["-I", "-w", "\nurl_effective: %{url_effective}\n"]
        header_cmd = [self.curl] + self.config_args + base_args + self._cookie_args + header_args

        header_process = subprocess.run(
            header_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
        )
        if header_process.returncode != 0:
            check_curl_code(header_process.returncode)
        headers_raw = header_process.stdout.decode("utf-8")

        headers = http.client.HTTPMessage()
        for line in headers_raw.splitlines():
            if ": " in line:
                key, value = line.split(": ", 1)
                headers[key.strip()] = value.strip()

        effective_url = headers.get("url_effective", url)
        return headers, effective_url

    def _start_body_read(self) -> None:
        base_args = base_curl_fetch_args(
            self._url, self._timeout, headers=False, status_bar=False, user_agent=SPACK_USER_AGENT
        )
        body_cmd = [self.curl] + self.config_args + ["-C", "-"] + base_args + self._cookie_args
        self._body_process = subprocess.Popen(body_cmd, stdout=subprocess.PIPE)

    def _read_body_chunk(self, size: int) -> bytes:
        assert self._body_process is not None, "body process was not started"
        assert self._body_process.stdout is not None, "stdout of curl process is None"
        return self._body_process.stdout.read(size)

    def _finalize_body_read(self) -> None:
        assert self._body_process is not None, "body process was not started"
        self._body_process.wait()
        check_curl_code(self._body_process.returncode)
        # Reset to uninitialized state
        self._timeout, self._url, self._body_process = 0, "", None

    @property
    def curl(self) -> str:
        if CurlDownloader._curl_exe is None:
            CurlDownloader._curl_exe = which_string("curl", required=True)
        return CurlDownloader._curl_exe

    @property
    def _cookie_args(self) -> List[str]:
        """Arguments to pass to curl to use a cookie."""
        if self.cookie:
            return ["-j", "-b", self.cookie]
        return []


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
        headers: http.client.HTTPMessage,
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
    content_types = download_info.headers.get("Content-Type")
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
