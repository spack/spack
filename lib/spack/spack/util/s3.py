# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import six.moves.urllib.parse as urllib_parse

import spack
import spack.util.url as url_util


def create_s3_session(url):
    parsed_url = url_util.parse(url)
    if parsed_url.scheme != 's3':
        raise ValueError(
                'Can not create S3 session from URL with scheme: {}'.format(
                    parsed_url.scheme))

    # NOTE(opadron): import boto and friends as late as possible.  We don't
    # want to require boto as a dependency unless the user actually wants to
    # access S3 mirrors.
    from boto3 import Session
    kwargs = {}

    if hasattr(parsed_url, 's3_profile'):
        kwargs['profile_name'] = parsed_url.s3_profile

    elif (hasattr(parsed_url, 's3_access_key_id') and
            hasattr(parsed_url, 's3_secret_access_key')):
        kwargs['aws_access_key_id'] = parsed_url.s3_access_key_id
        kwargs['aws_secret_access_key'] = parsed_url.s3_secret_access_key

    session = Session(**kwargs)

    s3_client_args = {"use_ssl": spack.config.get('config:verify_ssl')}

    endpoint_url = parsed_url.netloc
    if endpoint_url:
        if urllib_parse.urlparse(endpoint_url, scheme=None).scheme is None:
            endpoint_url = '://'.join(('https', endpoint_url))

        s3_client_args['endpoint_url'] = endpoint_url

    # if no access credentials provided above, then access anonymously
    if not session.get_credentials():
        from botocore import UNSIGNED
        from botocore.client import Config

        s3_client_args["config"] = Config(signature_version=UNSIGNED)

    return session.client('s3', **s3_client_args)
