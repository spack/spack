# TODO: This will be merged into the buildcache command once
# everything is working.

import argparse
import os
import sys

have_boto3_support=False
try:
    import boto3
    have_boto3_support=True
except Exception:
    pass

import llnl.util.tty as tty

import spack.cmd
import spack.config
import spack.repo
import spack.store
from spack.paths import etc_path
from spack.spec import Spec
from spack.util.spec_set import CombinatorialSpecSet

import spack.binary_distribution as bindist


description = "temporary command to upload buildcaches to 's3.spack.io'"
section = "packaging"
level = "long"


def setup_parser(subparser):
    subparser.add_argument('-s', '--spec', default=None,
        help='Spec to upload')

    subparser.add_argument('-b', '--base-dir', default=None,
        help='Path to root of buildcaches')

    subparser.add_argument('-e', '--endpoint-url',
        default='https://s3.spack.io', help='URL of mirror')


def wip_upload_spec(parser, args):
    if not have_boto3_support:
        tty.error('boto3 module not available')
        sys.exit(1)

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

    session = boto3.Session()
    # print('you provided a url: {0}'.format(args.endpoint_url))
    # s3 = session.resource('s3', endpoint_url=args.endpoint_url)
    s3 = session.resource('s3')

    bucket_names = []
    for bucket in s3.buckets.all():
        bucket_names.append(bucket.name)

    if len(bucket_names) > 1:
        tty.error('More than one bucket associated with credentials')
        sys.exit(1)

    bucket_name = bucket_names[0]
    build_cache_dir = bindist.build_cache_relative_path()

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
