# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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

description = "create, download and install binary packages"
section = "packaging"
level = "long"


def setup_parser(subparser):
    setup_parser.parser = subparser
    subparsers = subparser.add_subparsers(help='buildcache sub-commands')

    create = subparsers.add_parser('create', help=createtarball.__doc__)
    create.add_argument('-r', '--rel', action='store_true',
                        help="make all rpaths relative" +
                             " before creating tarballs.")
    create.add_argument('-f', '--force', action='store_true',
                        help="overwrite tarball if it exists.")
    create.add_argument('-u', '--unsigned', action='store_true',
                        help="create unsigned buildcache" +
                             " tarballs for testing")
    create.add_argument('-a', '--allow_root', action='store_true',
                        help="allow install root string in binary files " +
                             "after RPATH substitution")
    create.add_argument('-k', '--key', metavar='key',
                        type=str, default=None,
                        help="Key for signing.")
    create.add_argument('-d', '--directory', metavar='directory',
                        type=str, default='.',
                        help="directory in which to save the tarballs.")
    create.add_argument('--no-rebuild-index', action='store_true',
                        default=False, help="skip rebuilding index after " +
                                            "building package(s)")
    create.add_argument('--cdash-build-id', default=None,
                        help="If provided, a .cdashid file will be written " +
                        "alongside .spec.yaml")
    create.add_argument(
        'packages', nargs=argparse.REMAINDER,
        help="specs of packages to create buildcache for")
    create.set_defaults(func=createtarball)

    install = subparsers.add_parser('install', help=installtarball.__doc__)
    install.add_argument('-f', '--force', action='store_true',
                         help="overwrite install directory if it exists.")
    install.add_argument('-m', '--multiple', action='store_true',
                         help="allow all matching packages ")
    install.add_argument('-a', '--allow_root', action='store_true',
                         help="allow install root string in binary files " +
                              "after RPATH substitution")
    install.add_argument('-u', '--unsigned', action='store_true',
                         help="install unsigned buildcache" +
                              " tarballs for testing")
    install.add_argument(
        'packages', nargs=argparse.REMAINDER,
        help="specs of packages to install buildcache for")
    install.set_defaults(func=installtarball)

    listcache = subparsers.add_parser('list', help=listspecs.__doc__)
    listcache.add_argument('-f', '--force', action='store_true',
                           help="force new download of specs")
    listcache.add_argument(
        'packages', nargs=argparse.REMAINDER,
        help="specs of packages to search for")
    listcache.set_defaults(func=listspecs)

    dlkeys = subparsers.add_parser('keys', help=getkeys.__doc__)
    dlkeys.add_argument(
        '-i', '--install', action='store_true',
        help="install Keys pulled from mirror")
    dlkeys.add_argument(
        '-t', '--trust', action='store_true',
        help="trust all downloaded keys")
    dlkeys.add_argument('-f', '--force', action='store_true',
                        help="force new download of keys")
    dlkeys.set_defaults(func=getkeys)

    # Check if binaries need to be rebuilt on remote mirror
    check = subparsers.add_parser('check', help=check_binaries.__doc__)
    check.add_argument(
        '-m', '--mirror-url', default=None,
        help='Override any configured mirrors with this mirror url')

    check.add_argument(
        '-o', '--output-file', default=None,
        help='File where rebuild info should be written')

    # used to construct scope arguments below
    scopes = spack.config.scopes()
    scopes_metavar = spack.config.scopes_metavar

    check.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        default=spack.config.default_modify_scope(),
        help="configuration scope containing mirrors to check")

    check.add_argument(
        '-s', '--spec', default=None,
        help='Check single spec instead of building from release specs file')

    check.add_argument(
        '-y', '--spec-yaml', default=None,
        help='Check single spec from yaml file instead of building from release specs file')

    check.add_argument(
        '-', '--no-index', action='store_true', default=False,
        help='Do not use buildcache index, instead retrieve .spec.yaml files')
    check.set_defaults(func=check_binaries)

    # Download tarball and spec.yaml
    dltarball = subparsers.add_parser('download', help=get_tarball.__doc__)
    dltarball.add_argument(
        '-s', '--spec', default=None,
        help="Download built tarball for spec from mirror")
    dltarball.add_argument(
        '-y', '--spec-yaml', default=None,
        help="Download built tarball for spec (from yaml file) from mirror")
    dltarball.add_argument(
        '-p', '--path', default=None,
        help="Path to directory where tarball should be downloaded")
    dltarball.set_defaults(func=get_tarball)

    # Get buildcache name
    getbuildcachename = subparsers.add_parser('get-buildcache-name',
                                    help=get_buildcache_name.__doc__)
    getbuildcachename.add_argument(
        '-s', '--spec', default=None,
        help='Spec string for which buildcache name is desired')
    getbuildcachename.add_argument(
        '-y', '--spec-yaml', default=None,
        help='Path to spec yaml file for which buildcache name is desired')
    getbuildcachename.set_defaults(func=get_buildcache_name)

    # Given the root spec, save the yaml of the dependent spec to a file
    saveyaml = subparsers.add_parser('save-yaml',
                                    help=save_dependent_spec_yaml.__doc__)
    saveyaml.add_argument(
        '-r', '--root-spec', default=None,
        help='Root spec of dependent spec')
    saveyaml.add_argument(
        '-s', '--spec', default=None,
        help='Dependent spec for which saved yaml is desired')
    saveyaml.add_argument(
        '-y', '--yaml-path', default=None,
        help='Path to file where spec yaml should be saved')
    saveyaml.set_defaults(func=save_dependent_spec_yaml)

    # Put buildcache entry somewhere (file system or s3)
    put = subparsers.add_parser('put', help=put_buildcache.__doc__)
    put.add_argument('-d', '--directory', default='.',
                     help="Location of mirror directory, similar to 'create'")
    put.add_argument('-s', '--spec', default=None,
                     help="Spec indicating which binary to put")
    put.add_argument('-m', '--mirror-name', default=None,
                     help="Name of mirror where binary should be pushed")
    put.add_argument('-p', '--profile', default=None,
                     help="Name of AWS profile")
    put.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        default=spack.config.default_modify_scope(),
        help="configuration scope giving possible mirrors")
    put.set_defaults(func=put_buildcache)


def find_matching_specs(pkgs, allow_multiple_matches=False, force=False):
    """Returns a list of specs matching the not necessarily
       concretized specs given from cli

    Args:
        specs: list of specs to be matched against installed packages
        allow_multiple_matches : if True multiple matches are admitted

    Return:
        list of specs
    """
    # List of specs that match expressions given via command line
    specs_from_cli = []
    has_errors = False
    specs = spack.cmd.parse_specs(pkgs)
    for spec in specs:
        matching = spack.store.db.query(spec)
        # For each spec provided, make sure it refers to only one package.
        # Fail and ask user to be unambiguous if it doesn't
        if not allow_multiple_matches and len(matching) > 1:
            tty.error('%s matches multiple installed packages:' % spec)
            for match in matching:
                tty.msg('"%s"' % match.format())
            has_errors = True

        # No installed package matches the query
        if len(matching) == 0 and spec is not any:
            tty.error('{0} does not match any installed packages.'.format(
                spec))
            has_errors = True

        specs_from_cli.extend(matching)
    if has_errors:
        tty.die('use one of the matching specs above')

    return specs_from_cli


def match_downloaded_specs(pkgs, allow_multiple_matches=False, force=False):
    """Returns a list of specs matching the not necessarily
       concretized specs given from cli

    Args:
        specs: list of specs to be matched against buildcaches on mirror
        allow_multiple_matches : if True multiple matches are admitted

    Return:
        list of specs
    """
    # List of specs that match expressions given via command line
    specs_from_cli = []
    has_errors = False
    specs = bindist.get_specs(force)
    for pkg in pkgs:
        matches = []
        tty.msg("buildcache spec(s) matching %s \n" % pkg)
        for spec in sorted(specs):
            if pkg.startswith('/'):
                pkghash = pkg.replace('/', '')
                if spec.dag_hash().startswith(pkghash):
                    matches.append(spec)
            else:
                if spec.satisfies(pkg):
                    matches.append(spec)
        # For each pkg provided, make sure it refers to only one package.
        # Fail and ask user to be unambiguous if it doesn't
        if not allow_multiple_matches and len(matches) > 1:
            tty.error('%s matches multiple downloaded packages:' % pkg)
            for match in matches:
                tty.msg('"%s"' % match.format())
            has_errors = True

        # No downloaded package matches the query
        if len(matches) == 0:
            tty.error('%s does not match any downloaded packages.' % pkg)
            has_errors = True

        specs_from_cli.extend(matches)
    if has_errors:
        tty.die('use one of the matching specs above')

    return specs_from_cli


def createtarball(args):
    """create a binary package from an existing install"""
    if not args.packages:
        tty.die("build cache file creation requires at least one" +
                " installed package argument")
    pkgs = set(args.packages)
    specs = set()
    outdir = '.'
    if args.directory:
        outdir = args.directory
    signkey = None
    if args.key:
        signkey = args.key

    matches = find_matching_specs(pkgs, False, False)
    for match in matches:
        if match.external or match.virtual:
            tty.msg('skipping external or virtual spec %s' %
                    match.format())
        else:
            tty.msg('adding matching spec %s' % match.format())
            specs.add(match)
            tty.msg('recursing dependencies')
            for d, node in match.traverse(order='post',
                                          depth=True,
                                          deptype=('link', 'run')):
                if node.external or node.virtual:
                    tty.msg('skipping external or virtual dependency %s' %
                            node.format())
                else:
                    tty.msg('adding dependency %s' % node.format())
                    specs.add(node)

    tty.msg('writing tarballs to %s/build_cache' % outdir)

    for spec in specs:
        tty.msg('creating binary cache file for package %s ' % spec.format())
        spec.concretize()
        bindist.build_tarball(spec, outdir, args.force, args.rel,
                              args.unsigned, args.allow_root, signkey,
                              not args.no_rebuild_index, args.cdash_build_id)


def installtarball(args):
    """install from a binary package"""
    if not args.packages:
        tty.die("build cache file installation requires" +
                " at least one package spec argument")
    pkgs = set(args.packages)
    matches = match_downloaded_specs(pkgs, args.multiple, args.force)

    for match in matches:
        install_tarball(match, args)


def install_tarball(spec, args):
    s = Spec(spec)
    if s.external or s.virtual:
        tty.warn("Skipping external or virtual package %s" % spec.format())
        return
    for d in s.dependencies(deptype=('link', 'run')):
        tty.msg("Installing buildcache for dependency spec %s" % d)
        install_tarball(d, args)
    package = spack.repo.get(spec)
    if s.concrete and package.installed and not args.force:
        tty.warn("Package for spec %s already installed." % spec.format())
    else:
        tarball = bindist.download_tarball(spec)
        if tarball:
            tty.msg('Installing buildcache for spec %s' % spec.format())
            bindist.extract_tarball(spec, tarball, args.allow_root,
                                    args.unsigned, args.force)
            spack.hooks.post_install(spec)
            spack.store.store.reindex()
        else:
            tty.die('Download of binary cache file for spec %s failed.' %
                    spec.format())


def listspecs(args):
    """list binary packages available from mirrors"""
    specs = bindist.get_specs(args.force)
    if args.packages:
        pkgs = set(args.packages)
        for pkg in pkgs:
            tty.msg("buildcache spec(s) matching " +
                    "%s and commands to install them" % pkgs)
            for spec in sorted(specs):
                if spec.satisfies(pkg):
                    tty.msg('Enter\nspack buildcache install /%s\n' %
                            spec.dag_hash(7) +
                            ' to install "%s"' %
                            spec.format())
    else:
        tty.msg("buildcache specs and commands to install them")
        for spec in sorted(specs):
            tty.msg('Enter\nspack buildcache install /%s\n' %
                    spec.dag_hash(7) +
                    ' to install "%s"' %
                    spec.format())


def getkeys(args):
    """get public keys available on mirrors"""
    bindist.get_keys(args.install, args.trust, args.force)


def check_binaries(args):
    """Check specs (either a single spec from --spec, or else the full set
    of release specs) against remote binary mirror(s) to see if any need
    to be rebuilt.
    """
    if args.spec or args.spec_yaml:
        specs = [get_concrete_spec(args)]
    else:
        release_specs_path = os.path.join(
            etc_path, 'spack', 'defaults', 'release.yaml')
        spec_set = CombinatorialSpecSet.from_file(release_specs_path)
        specs = [spec for spec in spec_set]

    if not specs:
        tty.msg('No specs provided, exiting.')
        sys.exit(0)

    for spec in specs:
        spec.concretize()

    # Next see if there are any configured binary mirrors
    configured_mirrors = spack.config.get('mirrors', scope=args.scope)

    if args.mirror_url:
        configured_mirrors = {'additionalMirrorUrl': args.mirror_url}

    if not configured_mirrors:
        tty.msg('No mirrors provided, exiting.')
        sys.exit(0)

    no_index = args.no_index
    output_file = args.output_file

    sys.exit(bindist.check_specs_against_mirrors(
        configured_mirrors, specs, no_index, output_file))


def get_tarball(args):
    """Download buildcache entry from remote mirror to local folder"""
    if not args.spec and not args.spec_yaml:
        tty.msg('No specs provided, exiting.')
        sys.exit(0)

    if not args.path:
        tty.msg('No download path provided, exiting')
        sys.exit(0)

    spec = get_concrete_spec(args)
    bindist.download_buildcache_entry(spec, args.path)


def get_concrete_spec(args):
    spec_str = args.spec
    spec_yaml_path = args.spec_yaml

    if not spec_str and not spec_yaml_path:
        tty.msg('Must provide either spec string or path to ' +
            'yaml to concretize spec')
        sys.exit(1)

    if spec_str:
        try:
            spec = Spec(spec_str)
            spec.concretize()
        except Exception:
            tty.error('Unable to concrectize spec {0}'.format(args.spec))
            sys.exit(1)

        return spec

    with open(spec_yaml_path, 'r') as fd:
        return Spec.from_yaml(fd.read())


def get_buildcache_name(args):
    """Get name (prefix) of buildcache entries for this spec"""
    spec = get_concrete_spec(args)
    buildcache_name = bindist.tarball_name(spec, '')

    print('{0}'.format(buildcache_name))

    sys.exit(0)


def save_dependent_spec_yaml(args):
    """Get full spec relative to root spec and write it to a file"""
    if not args.root_spec:
        tty.msg('No root spec provided, exiting.')
        sys.exit(1)

    if not args.spec:
        tty.msg('No dependent spec provided, exiting.')
        sys.exit(1)

    if not args.yaml_path:
        tty.msg('No yaml path provided, exiting.')
        sys.exit(1)

    try:
        rootSpec = Spec(args.root_spec)
        rootSpec.concretize()
        spec = rootSpec
        if args.root_spec != args.spec:
            spec = rootSpec[args.spec]
    except Exception:
        tty.error('Unable to get dependent spec {0} from root spec {1}'.format(
            args.root_spec, args.spec))
        sys.exit(1)

    with open(args.yaml_path, 'w') as fd:
        fd.write(spec.to_yaml())

    sys.exit(0)


def mirror_buildcache_entry(client, spec,
                            local_mirror_dir, remote_mirror_url):
    # TODO:
    #   1) check remote mirror url to determine file or s3
    #   1a) If it's an s3 url and we don't have boto3 (have_boto3_support is
    #     false), then we need to fail gracefully with a message about
    #     installing it.
    #   2) for s3, infer bucket name from url
    #   3) look for spec in local_mirror_dir, try a buildcache
    #     create if the package isn't already there
    #   4) copy/push both the .spec.yaml and .spack files into place

    # root = os.getcwd()
    # filename = os.path.join(root, file)
    # client.upload_file(filename, bucket, key)
    # tty.msg("Uploaded %s to %s as %s" % (file, bucket, key))

    return True


def _get_s3_client(profile):
    """Create AWS s3 client"""
    if profile:
        session = boto3.Session(profile_name=profile)
        client = session.client('s3')
    else:
        client = boto3.client('s3')

    return client


def put_buildcache(args):
    """Put buildcache entry (binary package) to file system or s3 bucket"""
    if not args.spec:
        tty.msg('No specs provided, exiting.')
        sys.exit(1)

    try:
        spec = Spec(args.spec)
        spec.concretize()
    except Exception:
        tty.error('Unable to concrectize spec {0}'.format(args.spec))
        sys.exit(1)

    mirror_dir = args.directory

    if not args.mirror_name:
        tty.msg('Please provide name of mirror to push tarball')
        sys.exit(1)

    target_mirror_name = args.mirror_name
    configured_mirrors = spack.config.get('mirrors', scope=args.scope)

    if target_mirror_name not in configured_mirrors:
        tty.msg('Mirror {0} could not be found'.format(target_mirror_name))
        sys.exit(1)

    mirror_url = configured_mirrors[target_mirror_name]
    client = _get_s3_client(args.profile)
    success = mirror_buildcache_entry(
        client, spec, mirror_dir, mirror_url)

    if not success:
        sys.exit(1)

    sys.exit(0)


def buildcache(parser, args):
    if args.func:
        args.func(args)
