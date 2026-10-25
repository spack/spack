# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import codecs
import pathlib
import urllib
from typing import IO, Union

import spack.util.web as web_util

from .storage_base import StorageBase, storage


@storage("__default__")
@storage("http")
@storage("https")
class URLStore(StorageBase):

    def read(self, key: Union[str, pathlib.Path]) -> IO[str]:  # type: ignore[return-type]
        key_path = str(pathlib.Path(self.url.path) / key)
        key_url = urllib.parse.urljoin(urllib.parse.urlunparse(self.url), key_path)
        _, _, resp = web_util.read_from_url(key_url)
        return codecs.getreader("utf-8")(resp)  # type: ignore

    # Unimplemented methods
    #  -  write
    #  -  list
    #  -  delete
    #  -  stat
