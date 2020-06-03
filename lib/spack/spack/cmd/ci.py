# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
import sys

from six.moves.urllib.parse import urlencode

import llnl.util.tty as tty

import spack.binary_distribution as bindist
import spack.ci as spack_ci
import spack.cmd.buildcache as buildcache
import spack.environment as ev
import spack.hash_types as ht
import spack.util.executable as exe


description = "manage continuous integration pipelines"
section = "build"
level = "long"


def get_env_var(variable_name):
    if variable_name in os.environ:
        return os.environ.get(variable_name)
    return None


def setup_parser(subparser):
    setup_parser.parser = subparser
    subparsers = subparser.add_subparsers(help='CI sub-commands')

    # Dynamic generation of the jobs yaml from a spack environment
    generate = subparsers.add_parser('generate', help=ci_generate.__doc__)
    generate.add_argument(
        '--output-file', default=None,
        help="Absolute path to file where generated jobs file should be " +
             "written.  The default is .gitlab-ci.yml in the root of the " +
             "repository.")
    generate.add_argument(
        '--copy-to', default=None,
        help="Absolute path of additional location where generated jobs " +
             "yaml file should be copied.  Default is not to copy.")
    generate.add_argument(
        '--spack-repo', default=None,
        help="Provide a url for this argument if a custom spack repo " +
             "should be cloned as a step in each generated job.")
    generate.add_argument(
        '--spack-ref', default=None,
        help="Provide a git branch or tag if a custom spack branch " +
             "should be checked out as a step in each generated job.  " +
             "This argument is ignored if no --spack-repo is provided.")
    generate.set_defaults(func=ci_generate)

    # Check a spec against mirror. Rebuild, create buildcache and push to
    # mirror (if necessary).
    rebuild = subparsers.add_parser('rebuild', help=ci_rebuild.__doc__)
    rebuild.set_defaults(func=ci_rebuild)


def ci_generate(args):
    """Generate jobs file from a spack environment file containing CI info.
       Before invoking this command, you can set the environment variable
       SPACK_CDASH_AUTH_TOKEN to contain the CDash authorization token
       for creating a build group for the generated workload and registering
       all generated jobs under that build group.  If this environment
       variable is not set, no build group will be created on CDash."""
    env = ev.get_env(args, 'ci generate', required=True)

    output_file = args.output_file
    copy_yaml_to = args.copy_to
    spack_repo = args.spack_repo
    spack_ref = args.spack_ref

    if not output_file:
        gen_ci_dir = os.getcwd()
        output_file = os.path.join(gen_ci_dir, '.gitlab-ci.yml')
    else:
        gen_ci_dir = os.path.dirname(output_file)
        if not os.path.exists(gen_ci_dir):
            os.makedirs(gen_ci_dir)

    # Generate the jobs
    spack_ci.generate_gitlab_ci_yaml(
        env, True, output_file, spack_repo, spack_ref)

    if copy_yaml_to:
        copy_to_dir = os.path.dirname(copy_yaml_to)
        if not os.path.exists(copy_to_dir):
            os.makedirs(copy_to_dir)
        shutil.copyfile(output_file, copy_yaml_to)


def ci_rebuild(args):
    """This command represents a gitlab-ci job, corresponding to a single
       release spec.  As such it must first decide whether or not the spec it
       has been assigned to build is up to date on the remote binary mirror.
       If it is not (i.e. the full_hash of the spec as computed locally does
       not match the one stored in the metadata on the mirror), this script
       will build the package, create a binary cache for it, and then push all
       related files to the remote binary mirror.  This script also
       communicates with a remote CDash instance to share status on the package
       build process.

       The spec to be built by this job is represented by essentially two
       pieces of information: 1) a root spec (possibly already concrete, but
       maybe still needing to be concretized) and 2) a package name used to
       index that root spec (once the root is, for certain, concrete)."""
    env = ev.get_env(args, 'ci rebuild', required=True)
    yaml_root = ev.config_dict(env.yaml)

    # The following environment variables should defined in the CI
    # infrastructre (or some other external source) in the case that the
    # remote mirror is an S3 bucket.  The AWS keys are used to upload
    # buildcache entries to S3 using the boto3 api.
    #
    # AWS_ACCESS_KEY_ID
    # AWS_SECRET_ACCESS_KEY
    # S3_ENDPOINT_URL (only needed for non-AWS S3 implementations)
    #
    # If present, we will import the  SPACK_SIGNING_KEY using the
    # "spack gpg trust" command, so it can be used both for verifying
    # dependency buildcache entries and signing the buildcache entry we create
    # for our target pkg.
    #
    # SPACK_SIGNING_KEY

    ci_artifact_dir = get_env_var('CI_PROJECT_DIR')
    signing_key = get_env_var('SPACK_SIGNING_KEY')
    root_spec = get_env_var('SPACK_ROOT_SPEC')
    job_spec_pkg_name = get_env_var('SPACK_JOB_SPEC_PKG_NAME')
    compiler_action = get_env_var('SPACK_COMPILER_ACTION')
    cdash_build_name = get_env_var('SPACK_CDASH_BUILD_NAME')
    related_builds = get_env_var('SPACK_RELATED_BUILDS_CDASH')
    pr_env_var = get_env_var('SPACK_IS_PR_PIPELINE')

    gitlab_ci = None
    if 'gitlab-ci' in yaml_root:
        gitlab_ci = yaml_root['gitlab-ci']

    if not gitlab_ci:
        tty.die('spack ci rebuild requires an env containing gitlab-ci cfg')

    enable_cdash = False
    if 'cdash' in yaml_root:
        enable_cdash = True
        ci_cdash = yaml_root['cdash']
        job_spec_buildgroup = ci_cdash['build-group']
        cdash_base_url = ci_cdash['url']
        cdash_project = ci_cdash['project']
        proj_enc = urlencode({'project': cdash_project})
        eq_idx = proj_enc.find('=') + 1
        cdash_project_enc = proj_enc[eq_idx:]
        cdash_site = ci_cdash['site']
        tty.debug('cdash_base_url = {0}'.format(cdash_base_url))
        tty.debug('cdash_project = {0}'.format(cdash_project))
        tty.debug('cdash_project_enc = {0}'.format(cdash_project_enc))
        tty.debug('cdash_build_name = {0}'.format(cdash_build_name))
        tty.debug('cdash_site = {0}'.format(cdash_site))
        tty.debug('related_builds = {0}'.format(related_builds))
        tty.debug('job_spec_buildgroup = {0}'.format(job_spec_buildgroup))

    remote_mirror_url = None
    if 'mirrors' in yaml_root:
        ci_mirrors = yaml_root['mirrors']
        mirror_urls = [url for url in ci_mirrors.values()]
        remote_mirror_url = mirror_urls[0]

    if not remote_mirror_url:
        tty.die('spack ci rebuild requires an env containing a mirror')

    tty.debug('ci_artifact_dir = {0}'.format(ci_artifact_dir))
    tty.debug('root_spec = {0}'.format(root_spec))
    tty.debug('remote_mirror_url = {0}'.format(remote_mirror_url))
    tty.debug('job_spec_pkg_name = {0}'.format(job_spec_pkg_name))
    tty.debug('compiler_action = {0}'.format(compiler_action))

    spack_cmd = exe.which('spack')

    cdash_report_dir = os.path.join(ci_artifact_dir, 'cdash_report')
    temp_dir = os.path.join(ci_artifact_dir, 'jobs_scratch_dir')
    job_log_dir = os.path.join(temp_dir, 'logs')
    spec_dir = os.path.join(temp_dir, 'specs')

    local_mirror_dir = os.path.join(ci_artifact_dir, 'local_mirror')
    build_cache_dir = os.path.join(local_mirror_dir, 'build_cache')

    spack_is_pr_pipeline = True if pr_env_var == 'True' else False

    enable_artifacts_mirror = False
    artifact_mirror_url = None
    if 'enable-artifacts-buildcache' in gitlab_ci:
        enable_artifacts_mirror = gitlab_ci['enable-artifacts-buildcache']
        if enable_artifacts_mirror or spack_is_pr_pipeline:
            # If this is a PR pipeline, we will override the setting to
            # make sure that artifacts buildcache is enabled.  Otherwise
            # jobs will not have binary deps available since we do not
            # allow pushing binaries to remote mirror during PR pipelines
            enable_artifacts_mirror = True
            artifact_mirror_url = 'file://' + local_mirror_dir
            mirror_msg = 'artifact buildcache enabled, mirror url: {0}'.format(
                artifact_mirror_url)
            tty.debug(mirror_msg)

    # Clean out scratch directory from last stage
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    if os.path.exists(cdash_report_dir):
        shutil.rmtree(cdash_report_dir)

    os.makedirs(job_log_dir)
    os.makedirs(spec_dir)

    job_spec_yaml_path = os.path.join(
        spec_dir, '{0}.yaml'.format(job_spec_pkg_name))
    job_log_file = os.path.join(job_log_dir, 'pipeline_log.txt')

    cdash_build_id = None
    cdash_build_stamp = None

    with open(job_log_file, 'w') as log_fd:
        os.dup2(log_fd.fileno(), sys.stdout.fileno())
        os.dup2(log_fd.fileno(), sys.stderr.fileno())

        current_directory = os.getcwd()
        tty.debug('Current working directory: {0}, Contents:'.format(
            current_directory))
        directory_list = os.listdir(current_directory)
        for next_entry in directory_list:
            tty.debug('  {0}'.format(next_entry))

        # Make a copy of the environment file, so we can overwrite the changed
        # version in between the two invocations of "spack install"
        env_src_path = os.path.join(current_directory, 'spack.yaml')
        env_dst_path = os.path.join(current_directory, 'spack.yaml_BACKUP')
        shutil.copyfile(env_src_path, env_dst_path)

        tty.debug('job concrete spec path: {0}'.format(job_spec_yaml_path))

        if signing_key:
            spack_ci.import_signing_key(signing_key)

        spack_ci.configure_compilers(compiler_action)

        spec_map = spack_ci.get_concrete_specs(
            root_spec, job_spec_pkg_name, related_builds, compiler_action)

        job_spec = spec_map[job_spec_pkg_name]

        tty.debug('Here is the concrete spec: {0}'.format(job_spec))

        with open(job_spec_yaml_path, 'w') as fd:
            fd.write(job_spec.to_yaml(hash=ht.build_hash))

        tty.debug('Done writing concrete spec')

        # DEBUG
        with open(job_spec_yaml_path) as fd:
            tty.debug('Wrote spec file, read it back.  Contents:')
            tty.debug(fd.read())

        # DEBUG the root spec
        root_spec_yaml_path = os.path.join(spec_dir, 'root.yaml')
        with open(root_spec_yaml_path, 'w') as fd:
            fd.write(spec_map['root'].to_yaml(hash=ht.build_hash))

        if bindist.needs_rebuild(job_spec, remote_mirror_url, True):
            # Binary on remote mirror is not up to date, we need to rebuild
            # it.
            #
            # FIXME: ensure mirror precedence causes this local mirror to
            # be chosen ahead of the remote one when installing deps
            if enable_artifacts_mirror:
                mirror_add_output = spack_cmd(
                    'mirror', 'add', 'local_mirror', artifact_mirror_url)
                tty.debug('spack mirror add:')
                tty.debug(mirror_add_output)

            mirror_list_output = spack_cmd('mirror', 'list')
            tty.debug('listing spack mirrors:')
            tty.debug(mirror_list_output)

            # 2) build up install arguments
            install_args = ['-d', '-v', '-k', 'install', '--keep-stage']

            # 3) create/register a new build on CDash (if enabled)
            cdash_args = []
            if enable_cdash:
                tty.debug('Registering build with CDash')
                (cdash_build_id,
                    cdash_build_stamp) = spack_ci.register_cdash_build(
                    cdash_build_name, cdash_base_url, cdash_project,
                    cdash_site, job_spec_buildgroup)

                cdash_upload_url = '{0}/submit.php?project={1}'.format(
                    cdash_base_url, cdash_project_enc)

                cdash_args = [
                    '--cdash-upload-url', cdash_upload_url,
                    '--cdash-build', cdash_build_name,
                    '--cdash-site', cdash_site,
                    '--cdash-buildstamp', cdash_build_stamp,
                ]

            spec_cli_arg = [job_spec_yaml_path]

            tty.debug('Installing package')

            try:
                # Two-pass install is intended to avoid spack trying to
                # install from buildcache even though the locally computed
                # full hash is different than the one stored in the spec.yaml
                # file on the remote mirror.
                first_pass_args = install_args + [
                    '--cache-only',
                    '--only',
                    'dependencies',
                ]
                first_pass_args.extend(spec_cli_arg)
                tty.debug('First pass install arguments: {0}'.format(
                    first_pass_args))
                spack_cmd(*first_pass_args)

                # Overwrite the changed environment file so it doesn't
                # the next install invocation.
                shutil.copyfile(env_dst_path, env_src_path)

                second_pass_args = install_args + [
                    '--no-cache',
                    '--only',
                    'package',
                ]
                second_pass_args.extend(cdash_args)
                second_pass_args.extend(spec_cli_arg)
                tty.debug('Second pass install arguments: {0}'.format(
                    second_pass_args))
                spack_cmd(*second_pass_args)
            except Exception as inst:
                tty.error('Caught exception during install:')
                tty.error(inst)

            spack_ci.copy_stage_logs_to_artifacts(job_spec, job_log_dir)

            # 4) create buildcache on remote mirror, but not if this is
            # running to test a spack PR
            if not spack_is_pr_pipeline:
                spack_ci.push_mirror_contents(
                    env, job_spec, job_spec_yaml_path, remote_mirror_url,
                    cdash_build_id)

            # 5) create another copy of that buildcache on "local artifact
            # mirror" (only done if cash reporting is enabled)
            spack_ci.push_mirror_contents(env, job_spec, job_spec_yaml_path,
                                          artifact_mirror_url, cdash_build_id)

            # 6) relate this build to its dependencies on CDash (if enabled)
            if enable_cdash:
                spack_ci.relate_cdash_builds(
                    spec_map, cdash_base_url, cdash_build_id, cdash_project,
                    artifact_mirror_url or remote_mirror_url)
        else:
            # There is nothing to do here unless "local artifact mirror" is
            # enabled, in which case, we need to download the buildcache to
            # the local artifacts directory to be used by dependent jobs in
            # subsequent stages
            tty.debug('No need to rebuild {0}'.format(job_spec_pkg_name))
            if enable_artifacts_mirror:
                tty.debug('Getting {0} buildcache'.format(job_spec_pkg_name))
                tty.debug('Downloading to {0}'.format(build_cache_dir))
                buildcache.download_buildcache_files(
                    job_spec, build_cache_dir, True, remote_mirror_url)


def ci(parser, args):
    if args.func:
        args.func(args)
