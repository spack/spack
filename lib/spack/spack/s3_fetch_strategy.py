# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


################################################################################
### TODO(opadron): REMEMBER TO MERGE THIS BACK IN WITH fetch_strategy.py! ######
################################################################################

import os.path

from functools import wraps
from shutil import copyfileobj

from llnl.util.filesystem import working_dir
from llnl.util import tty

import spack
import spack.util.url as url_util
import spack.util.web as web_util


# TODO(opadron): remove import when merging
from spack.fetch_strategy import URLFetchStrategy


def _needs_stage(fun):
    """Many methods on fetch strategies require a stage to be set
       using set_stage().  This decorator adds a check for self.stage."""

    @wraps(fun)
    def wrapper(self, *args, **kwargs):
        if not self.stage:
            raise NoStageError(fun)
        return fun(self, *args, **kwargs)

    return wrapper


class S3FetchStrategy(URLFetchStrategy):
    """FetchStrategy that pulls from an S3 bucket.
    """
    enabled = True
    url_attr = 's3'

    def __init__(self, *args, **kwargs):
        try:
            super(S3FetchStrategy, self).__init__(*args, **kwargs)
        except ValueError:
            if not kwargs.get('url'):
                raise ValueError("S3FetchStrategy requires a url for fetching.")

    @_needs_stage
    def fetch(self):
        if self.archive_file:
            tty.msg("Already downloaded %s" % self.archive_file)
            return

        parsed_url = url_util.parse(self.url)
        if parsed_url.scheme != 's3':
            raise ValueError('S3FetchStrategy can only fetch from s3:// urls.')

        save_file = getattr(self.stage, "save_filename", None)
        tty.msg("Fetching %s" % self.url)

        basename = os.path.basename(parsed_url.path)

        with working_dir(self.stage.path):
            _, headers, stream = web_util.read_from_url(self.url)

            with open(basename, 'wb') as f:
                copyfileobj(stream, f)

            content_type = headers['ContentType']

        if content_type == 'text/html':
            msg = ("The contents of {0} look like HTML. Either the URL "
                   "you are trying to use does not exist or you have an "
                   "internet gateway issue. You can remove the bad archive "
                   "using 'spack clean <package>', then try again using "
                   "the correct URL.")

            tty.warn(msg.format(self.archive_file or "the archive"))

        if self.stage.save_filename:
            os.rename(
                    os.path.join(self.stage.path, basename),
                    self.stage.save_filename)

        if not self.archive_file:
            raise FailedDownloadError(self.url)
