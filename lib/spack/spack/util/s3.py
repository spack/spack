# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import six.moves.urllib.parse as urllib_parse

import spack
import spack.util.url as url_util


def get_mirror_connection(url, url_type="push"):
    connection = {}
    # Try to find a mirror for potential connection information
    for mirror in spack.mirror.MirrorCollection().values():
        if "%s://%s" % (url.scheme, url.netloc) == mirror.push_url:
            connection = mirror.to_dict()[url_type]
    return connection


def _parse_s3_endpoint_url(endpoint_url):
    if not urllib_parse.urlparse(endpoint_url, scheme='').scheme:
        endpoint_url = '://'.join(('https', endpoint_url))

    return endpoint_url


def get_mirror_s3_connection_info(connection):
    s3_connection = {}

    s3_connection_is_dict = connection and isinstance(connection, dict)
    if s3_connection_is_dict:
        if connection.get("access_token"):
            s3_connection["aws_session_token"] = connection["access_token"]
        if connection.get("access_pair"):
            s3_connection["aws_access_key_id"] = connection["access_pair"][0]
            s3_connection["aws_secret_access_key"] = connection["access_pair"][1]
        if connection.get("profile"):
            s3_connection["profile_name"] = connection["profile"]

    s3_client_args = {"use_ssl": spack.config.get('config:verify_ssl')}

    endpoint_url = os.environ.get('S3_ENDPOINT_URL')
    if endpoint_url:
        s3_client_args['endpoint_url'] = _parse_s3_endpoint_url(endpoint_url)
    elif s3_connection_is_dict and connection.get("endpoint_url"):
        s3_client_args["endpoint_url"] = _parse_s3_endpoint_url(connection["endpoint_url"])  # noqa: E501

    return (s3_connection, s3_client_args)


def create_s3_session(url, connection={}):
    url = url_util.parse(url)
    if url.scheme != 's3':
        raise ValueError(
            'Can not create S3 session from URL with scheme: {SCHEME}'.format(
                SCHEME=url.scheme))

    # NOTE(opadron): import boto and friends as late as possible.  We don't
    # want to require boto as a dependency unless the user actually wants to
    # access S3 mirrors.
    from boto3 import Session  # type: ignore[import]
    from botocore.exceptions import ClientError  # type: ignore[import]

    s3_connection, s3_client_args = get_mirror_s3_connection_info(connection)

    session = Session(**s3_connection)
    # if no access credentials provided above, then access anonymously
    if not session.get_credentials():
        from botocore import UNSIGNED  # type: ignore[import]
        from botocore.client import Config  # type: ignore[import]

        s3_client_args["config"] = Config(signature_version=UNSIGNED)

    client = session.client('s3', **s3_client_args)
    client.ClientError = ClientError
    return client
