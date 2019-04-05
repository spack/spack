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
from spack.fetch_strategy import URLFetchStrategy
from spack.util.url import parse as urlparse


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
            if not kwargs.get('url', url):
                raise ValueError("S3FetchStrategy requires a url for fetching.")

    @_needs_stage
    def fetch(self):
        if self.archive_file:
            tty.msg("Already downloaded %s" % self.archive_file)
            return

        parsed_url = urlparse(self.url)
        if parsed_url.scheme != 's3':
            raise ValueError('S3FetchStrategy can only fetch from s3:// urls.')

        # NOTE(opadron): import boto and friends as late as possible.  We don't
        # want to require boto as a dependency unless the user actually wants to
        # access S3 mirrors.
        #
        # TODO(opadron): handle case where API endpoint is *not* AWS
        from boto3 import Session
        kwargs = {}

        if hasattr(parsed_url, 's3_profile'):
            kwargs['profile_name'] = parsed_url.s3_profile

        elif (hasattr(parsed_url, 's3_access_key_id') and
                hasattr(parsed_url, 's3_secret_access_key')):
            kwargs['aws_access_key_id'] = parsed_url.s3_access_key_id
            kwargs['aws_secret_access_key'] = parsed_url.s3_secret_access_key

        session = Session(**kwargs)
        s3_client_args = {
                "use_ssl": spack.config.get('config:verify_ssl')}

        # NOTE: if no access credentials provided above, then access anonymously
        if not session.get_credentials():
            from botocore import UNSIGNED
            from botocore.client import Config

            s3_client_args["config"] = Config(signature_version=UNSIGNED)

        s3 = session.client('s3', **s3_client_args)

        save_file = getattr(self.stage, "save_filename", None)
        tty.msg("Fetching %s" % self.url)

        basename = os.path.basename(parsed_url.path)

        with working_dir(self.stage.path):
            obj = s3.get_object(
                    Bucket=parsed_url.s3_bucket,
                    Key=parsed_url.path)

            with open(basename, 'wb') as f:
                copyfileobj(obj['Body'], f)

            content_type = obj['ContentType']

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
