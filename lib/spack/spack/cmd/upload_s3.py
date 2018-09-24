# TODO: This will be merged into the buildcache command once
# everything is working.

import argparse
import os
import re
import sys

have_boto3_support=False
try:
    import boto3
    import botocore
    have_boto3_support=True
except Exception:
    pass

import llnl.util.tty as tty

from spack.error import SpackError
from spack.spec import Spec


import spack.binary_distribution as bindist


description = "temporary command to upload buildcaches to 's3.spack.io'"
section = "packaging"
level = "long"


def setup_parser(subparser):
    setup_parser.parser = subparser
    subparsers = subparser.add_subparsers(help='upload-s3 sub-commands')

    # sub-command to upload a built spec to s3
    spec = subparsers.add_parser('spec', help=upload_spec.__doc__)

    spec.add_argument('-s', '--spec', default=None,
        help='Spec to upload')

    spec.add_argument('-b', '--base-dir', default=None,
        help='Path to root of buildcaches')

    spec.add_argument('-e', '--endpoint-url',
        default='https://s3.spack.io', help='URL of mirror')

    spec.set_defaults(func=upload_spec)

    # sub-command to update the index of a buildcache on s3
    index = subparsers.add_parser('index', help=update_index.__doc__)

    index.add_argument('-e', '--endpoint-url',
        default='https://s3.spack.io', help='URL of mirror')

    index.set_defaults(func=update_index)


def get_s3_session(endpoint_url):
    if not have_boto3_support:
        raise SpackError('boto3 module not available')

    session = boto3.Session()
    # print('you provided a url: {0}'.format(args.endpoint_url))
    # s3 = session.resource('s3', endpoint_url=args.endpoint_url)
    s3 = session.resource('s3')

    bucket_names = []
    for bucket in s3.buckets.all():
        bucket_names.append(bucket.name)

    if len(bucket_names) > 1:
        raise SpackError('More than one bucket associated with credentials')

    bucket_name = bucket_names[0]

    return s3, bucket_name


def update_index(args):
    """Update the index of an s3 buildcache"""
    s3, bucket_name = get_s3_session(args.endpoint_url)

    bucket = s3.Bucket(bucket_name)
    exists = True

    try:
        s3.meta.client.head_bucket(Bucket=bucket_name)
    except botocore.exceptions.ClientError as e:
        # If a client error is thrown, then check that it was a 404 error.
        # If it was a 404 error, then the bucket does not exist.
        error_code = e.response['Error']['Code']
        if error_code == '404':
            exists = False

    if not exists:
        tty.error('S3 bucket "{0}" does not exist'.format(bucket_name))
        sys.exit(1)

    build_cache_dir = bindist.build_cache_relative_path()

    spec_yaml_regex = re.compile('{0}/(.+\\.spec\\.yaml)$'.format(build_cache_dir))
    spack_regex = re.compile('{0}/([^/]+)/.+\\.spack$'.format(build_cache_dir))

    top_level_keys = set()

    for key in bucket.objects.all():
        m = spec_yaml_regex.search(key.key)
        if m:
            top_level_keys.add(m.group(1))
            print(m.group(1))
            continue

        m = spack_regex.search(key.key)
        if m:
            top_level_keys.add(m.group(1))
            print(m.group(1))
            continue

    contents = '<html>\n  <head>\n  </head>\n  <list>\n'

    for bucket_key in top_level_keys:
        contents += '    <li><a href="{0}"> {0}</a>\n'.format(bucket_key)

    contents += '  </list>\n</html>\n'
    index_key = os.path.join(build_cache_dir, 'index.html')

    print('Generated index:')
    print(contents)
    print('Pushing it to {0} -> {1}'.format(bucket_name, index_key))

    s3_obj = s3.Object(bucket_name, index_key)
    s3_obj.put(Body=contents, ACL='public-read')


def upload_spec(args):
    """Upload a spec to s3 bucket"""
    if not args.spec:
        tty.error('No specs provided, exiting.')
        sys.exit(1)

    if not args.base_dir:
        tty.error('No base directory for buildcache specified')
        sys.exit(1)

    try:
        spec = Spec(args.spec)
        spec.concretize()
    except Exception:
        tty.error('Unable to concrectize spec {0}'.format(args.spec))
        sys.exit(1)

    s3, bucket_name = get_s3_session(args.endpoint_url)

    build_cache_dir = os.path.join(
        'mirror', bindist.build_cache_relative_path())

    tarball_key = os.path.join(
        build_cache_dir, bindist.tarball_path_name(spec, '.spack'))
    tarball_path = os.path.join(args.base_dir, tarball_key)

    specfile_key = os.path.join(build_cache_dir,
        bindist.tarball_name(spec, '.spec.yaml'))
    specfile_path = os.path.join(args.base_dir, specfile_key)

    print(tarball_key)
    print(specfile_key)

    s3.meta.client.upload_file(tarball_path, bucket_name, tarball_key, ExtraArgs={'ACL':'public-read'})
    s3.meta.client.upload_file(specfile_path, bucket_name, specfile_key, ExtraArgs={'ACL':'public-read'})


def upload_s3(parser, args):
    if args.func:
        args.func(args)
