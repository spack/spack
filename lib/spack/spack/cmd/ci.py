# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
import sys

import llnl.util.tty as tty

import spack.binary_distribution as bindist
import spack.ci as spack_ci
import spack.cmd.buildcache as buildcache
import spack.environment as ev
import spack.hash_types as ht
# from spack.main import SpackCommand
import spack.repo
import spack.util.executable as exe


description = "Implement various pieces of CI pipeline for spack"
section = "packaging"     # TODO: where does this go?  new section?
level = "long"


# spack_buildcache = SpackCommand('buildcache')
# spack_mirror = SpackCommand('mirror')
# spack_install = SpackCommand('install')


def get_env_var(variable_name):
    if variable_name in os.environ:
        return os.environ.get(variable_name)
    return None


def find_nearest_repo_ancestor(somepath):
    if os.path.isdir(somepath):
        if '.git' in os.listdir(somepath):
            return somepath

        if somepath == '/':
            return None

    parent_path = os.path.dirname(somepath)

    return find_nearest_repo_ancestor(parent_path)


def setup_parser(subparser):
    setup_parser.parser = subparser
    subparsers = subparser.add_subparsers(help='CI sub-commands')

    start = subparsers.add_parser('start', help=ci_start.__doc__)
    start.add_argument(
        '--output-file', default=None,
        help="Absolute path to file where generated jobs file should be " +
             "written.  The default is ${SPACK_ROOT}/.gitlab-ci.yml")
    start.add_argument(
        '--env-repo', default=None,
        help="Url to repository where environment file lives.  The default " +
             "is the local spack repo.")
    start.add_argument(
        '--env-path', default='',
        help="Relative path to location of spack.yaml environment file, " +
             "where path is relative to root of environment repository.  " +
             "The default is the empty string, indicating the file lives at " +
             "the root of the repository.")
    start.add_argument(
        '--cdash-token', default=None,
        help="Token to use for registering a (possibly new) buildgroup with " +
             "CDash, assuming the spack ci environment file includes " +
             "reporting to one or more CDash instances.  The default is " +
             "None, which prevents CDash build group registration.")
    start.add_argument(
        '--copy-to', default=None,
        help="Absolute path of additional location where generated jobs " +
             "yaml file should be copied.  Default is not to copy.")
    start.add_argument(
        '--downstream-repo', default=None,
        help="Url to repository where commit containing jobs yaml file " +
             "should be pushed.")
    start.add_argument(
        '--branch-name', default='default-branch',
        help="Name of current branch, used in generation of pushed commit.")
    start.add_argument(
        '--commit-sha', default='none',
        help="SHA of current commit, used in generation of pushed commit.")
    start.set_defaults(func=ci_start)

    # Dynamic generation of the jobs yaml from a spack environment
    generate = subparsers.add_parser('generate', help=ci_generate.__doc__)
    generate.add_argument(
        '--output-file', default=None,
        help="Absolute path to file where generated jobs file should be " +
             "written.  The default is ${SPACK_ROOT}/.gitlab-ci.yml")
    generate.add_argument(
        '--env-repo', default=None,
        help="Url to repository where environment file lives.  The default " +
             "is the local spack repo.")
    generate.add_argument(
        '--env-path', default='',
        help="Relative path to location of spack.yaml environment file, " +
             "where path is relative to root of environment repository.  " +
             "The default is the empty string, indicating the file lives at " +
             "the root of the repository.")
    generate.add_argument(
        '--cdash-token', default=None,
        help="Token to use for registering a (possibly new) buildgroup with " +
             "CDash, assuming the spack ci environment file includes " +
             "reporting to one or more CDash instances.  The default is " +
             "None, which prevents CDash build group registration.")
    generate.add_argument(
        '--copy-to', default=None,
        help="Absolute path of additional location where generated jobs " +
             "yaml file should be copied.  Default is not to copy.")
    generate.set_defaults(func=ci_generate)

    # Commit and push jobs yaml to a downstream CI repo
    pushyaml = subparsers.add_parser('pushyaml', help=ci_pushyaml.__doc__)
    pushyaml.add_argument(
        '--downstream-repo', default=None,
        help="Url to repository where commit containing jobs yaml file " +
             "should be pushed.")
    pushyaml.add_argument(
        '--branch-name', default='default-branch',
        help="Name of current branch, used in generation of pushed commit.")
    pushyaml.add_argument(
        '--commit-sha', default='none',
        help="SHA of current commit, used in generation of pushed commit.")
    pushyaml.set_defaults(func=ci_pushyaml)

    # Check a spec against mirror. Rebuild, create buildcache and push to
    # mirror (if necessary).
    rebuild = subparsers.add_parser('rebuild', help=ci_rebuild.__doc__)
    rebuild.add_argument(
        '--downstream-repo', default=None,
        help="Url to repository where commit containing jobs yaml file " +
             "should be pushed.")
    rebuild.add_argument(
        '--branch-name', default='default-branch',
        help="Name of current branch, used in generation of pushed commit.")
    rebuild.add_argument(
        '--commit-sha', default='none',
        help="SHA of current commit, used in generation of pushed commit.")
    rebuild.set_defaults(func=ci_rebuild)


def ci_generate(args):
    """Generate jobs file from a spack environment file containing CI info"""
    env = ev.get_env(args, 'ci generate', required=True)

    output_file = args.output_file
    cdash_auth_token = args.cdash_token
    copy_yaml_to = args.copy_to

    if not output_file:
        gen_ci_dir = os.getcwd()
        output_file = os.path.join(gen_ci_dir, '.gitlab-ci.yml')
    else:
        gen_ci_dir = os.path.dirname(output_file)
        if not os.path.exists(gen_ci_dir):
            os.makedirs(gen_ci_dir)

    # Create a temporary working directory
    with spack_ci.TemporaryDirectory() as temp_dir:
        # Write cdash auth token to file system
        token_file = None
        if cdash_auth_token:
            token_file = os.path.join(temp_dir, cdash_auth_token)
            with open(token_file, 'w') as fd:
                fd.write('{0}\n'.format(cdash_auth_token))

        # Generate the jobs
        spack_ci.generate_gitlab_ci_yaml(env, token_file, True, output_file)

        if copy_yaml_to:
            copy_to_dir = os.path.dirname(copy_yaml_to)
            if not os.path.exists(copy_to_dir):
                os.makedirs(copy_to_dir)
            shutil.copyfile(output_file, copy_yaml_to)


def ci_pushyaml(args):
    """Push the generated jobs yaml file to a remote repository.  The file
       (.gitlab-ci.yaml) is expected to be in the current directory, which
       should be the root of the repository."""
    downstream_repo = args.downstream_repo
    branch_name = args.branch_name
    commit_sha = args.commit_sha

    if not downstream_repo:
        tty.die('No downstream repo to push to, exiting')

    working_dir = os.getcwd()
    jobs_yaml = os.path.join(working_dir, '.gitlab-ci.yml')
    git_dir = os.path.join(working_dir, '.git')

    if not os.path.exists(jobs_yaml):
        tty.die('.gitlab-ci.yml must exist in current directory')

    if not os.path.exists(git_dir):
        tty.die('.git directory must exist in current directory')

    # Create a temporary working directory
    with spack_ci.TemporaryDirectory() as temp_dir:
        git = exe.which('git', required=True)

        # Push a commit with the generated file to the downstream ci repo
        saved_git_dir = os.path.join(temp_dir, 'original-git-dir')

        shutil.move('.git', saved_git_dir)

        git('init', '.')

        git('config', 'user.email', 'robot@spack.io')
        git('config', 'user.name', 'Spack Build Bot')

        git('add', '.')

        tty.msg('git commit')
        commit_message = '{0} {1} ({2})'.format(
            'Auto-generated commit testing', branch_name, commit_sha)

        git('commit', '-m', '{0}'.format(commit_message))

        tty.msg('git push')
        git('remote', 'add', 'downstream', downstream_repo)
        push_to_branch = 'master:multi-ci-{0}'.format(branch_name)
        git('push', '--force', 'downstream', push_to_branch)

        shutil.rmtree('.git')
        shutil.move(saved_git_dir, '.git')
        git('reset', '--hard', 'HEAD')


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

    ci_artifact_dir = get_env_var('CI_PROJECT_DIR')
    signing_key = get_env_var('SPACK_SIGNING_KEY')
    spack_enable_cdash = get_env_var('SPACK_ENABLE_CDASH')
    root_spec = get_env_var('SPACK_ROOT_SPEC')
    remote_mirror_url = get_env_var('SPACK_MIRROR_URL')
    enable_artifacts_mirror = get_env_var('SPACK_ENABLE_ARTIFACTS_MIRROR')
    job_spec_pkg_name = get_env_var('SPACK_JOB_SPEC_PKG_NAME')
    compiler_action = get_env_var('SPACK_COMPILER_ACTION')
    cdash_base_url = get_env_var('SPACK_CDASH_BASE_URL')
    cdash_project = get_env_var('SPACK_CDASH_PROJECT')
    cdash_project_enc = get_env_var('SPACK_CDASH_PROJECT_ENC')
    cdash_build_name = get_env_var('SPACK_CDASH_BUILD_NAME')
    cdash_site = get_env_var('SPACK_CDASH_SITE')
    related_builds = get_env_var('SPACK_RELATED_BUILDS')
    job_spec_buildgroup = get_env_var('SPACK_JOB_SPEC_BUILDGROUP')

    enable_cdash = True if spack_enable_cdash == 'True' else False

    tty.msg('ci_artifact_dir = {0}'.format(ci_artifact_dir))
    tty.msg('enable_cdash = {0}'.format(enable_cdash))
    tty.msg('root_spec = {0}'.format(root_spec))
    tty.msg('remote_mirror_url = {0}'.format(remote_mirror_url))
    tty.msg('enable_artifacts_mirror = {0}'.format(enable_artifacts_mirror))
    tty.msg('job_spec_pkg_name = {0}'.format(job_spec_pkg_name))
    tty.msg('compiler_action = {0}'.format(compiler_action))
    tty.msg('cdash_base_url = {0}'.format(cdash_base_url))
    tty.msg('cdash_project = {0}'.format(cdash_project))
    tty.msg('cdash_project_enc = {0}'.format(cdash_project_enc))
    tty.msg('cdash_build_name = {0}'.format(cdash_build_name))
    tty.msg('cdash_site = {0}'.format(cdash_site))
    tty.msg('related_builds = {0}'.format(related_builds))
    tty.msg('job_spec_buildgroup = {0}'.format(job_spec_buildgroup))

    spack_cmd = exe.which('spack')

    os.environ['FORCE_UNSAFE_CONFIGURE'] = '1'

    # The following environment variables should have been provided by the CI
    # infrastructre (or some other external source) in the case that the remote
    # mirror is an S3 bucket.  The AWS keys are used to upload buildcache
    # entries to S3 using the boto3 api.  We import the SPACK_SIGNING_KEY using
    # the "gpg2 --import" command, it is used both for verifying dependency
    # buildcache entries and signing the buildcache entry we create for our
    # target pkg.
    #
    # AWS_ACCESS_KEY_ID
    # AWS_SECRET_ACCESS_KEY
    # AWS_ENDPOINT_URL (only needed for non-AWS S3 implementations)
    # SPACK_SIGNING_KEY

    cdash_report_dir = os.path.join(ci_artifact_dir, 'cdash_report')
    temp_dir = os.path.join(ci_artifact_dir, 'jobs_scratch_dir')
    job_log_dir = os.path.join(temp_dir, 'logs')
    spec_dir = os.path.join(temp_dir, 'specs')

    local_mirror_dir = os.path.join(ci_artifact_dir, 'local_mirror')
    build_cache_dir = os.path.join(local_mirror_dir, 'build_cache')

    artifact_mirror_url = 'file://' + local_mirror_dir

    # Clean out scratch directory from last stage
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    if os.path.exists(cdash_report_dir):
        shutil.rmtree(cdash_report_dir)

    os.makedirs(job_log_dir)
    os.makedirs(spec_dir)

    job_spec_yaml_path = os.path.join(
        spec_dir, '{0}.yaml'.format(job_spec_pkg_name))
    job_log_file = os.path.join(job_log_dir, 'cdash_log.txt')

    cdash_build_id = None
    cdash_build_stamp = None

    with open(job_log_file, 'w') as log_fd:
        os.dup2(log_fd.fileno(), sys.stdout.fileno())
        os.dup2(log_fd.fileno(), sys.stderr.fileno())

        tty.msg('job concrete spec path: {0}'.format(job_spec_yaml_path))

        spack_ci.import_signing_key(signing_key)

        real_compilers = spack_ci.configure_compilers(compiler_action)

        spec_map = spack_ci.get_concrete_specs(
            root_spec, job_spec_pkg_name, related_builds, compiler_action,
            real_compilers)

        job_spec = spec_map[job_spec_pkg_name]

        tty.msg('Here is the concrete spec: {0}'.format(job_spec))

        with open(job_spec_yaml_path, 'w') as fd:
            fd.write(job_spec.to_yaml(hash=ht.build_hash))

        tty.msg('Done writing concrete spec')

        # DEBUG
        with open(job_spec_yaml_path) as fd:
            tty.msg('Just wrote this file, reading it, here are the contents:')
            tty.msg(fd.read())

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
                spack_cmd('mirror', 'add', 'local_mirror', artifact_mirror_url)

            tty.msg('listing spack mirrors:')
            spack_cmd('mirror', 'list')

            # 2) build up install arguments
            install_args = ['-d', '-v', '-k', 'install', '--keep-stage']
            # install_args = ['--keep-stage']

            # 3) create/register a new build on CDash (if enabled)
            if enable_cdash:
                tty.msg('Registering build with CDash')
                (cdash_build_id,
                    cdash_build_stamp) = spack_ci.register_cdash_build(
                    cdash_build_name, cdash_base_url, cdash_project,
                    cdash_site, job_spec_buildgroup)

                cdash_upload_url = '{0}/submit.php?project={1}'.format(
                    cdash_base_url, cdash_project_enc)

                install_args.extend([
                    '--cdash-upload-url', cdash_upload_url,
                    '--cdash-build', cdash_build_name,
                    '--cdash-site', cdash_site,
                    '--cdash-buildstamp', cdash_build_stamp,
                ])

            install_args.extend(['-f', job_spec_yaml_path])

            tty.msg('Installing package')

            try:
                spack_cmd(*install_args)
                # spack_install(*install_args)
            except Exception as inst:
                tty.msg('Caught exception during install:')
                tty.msg(inst)

            job_pkg = spack.repo.get(job_spec)
            stage_dir = job_pkg.stage.path
            build_env_src = os.path.join(stage_dir, 'spack-build-env.txt')
            build_out_src = os.path.join(stage_dir, 'spack-build-out.txt')
            build_env_dst = os.path.join(job_log_dir, 'spack-build-env.txt')
            build_out_dst = os.path.join(job_log_dir, 'spack-build-out.txt')
            shutil.copyfile(build_env_src, build_env_dst)
            shutil.copyfile(build_out_src, build_out_dst)

            tty.msg('Creating buildcache')

            # 4) create buildcache on remote mirror
            buildcache._createtarball(
                env, job_spec_yaml_path, None, remote_mirror_url, None, True,
                True, False, False, True, False)

            if enable_cdash:
                tty.msg('Writing .cdashid ({0}) to remote mirror ({1})'.format(
                    cdash_build_id, remote_mirror_url))
                spack_ci.write_cdashid_to_mirror(
                    cdash_build_id, job_spec, remote_mirror_url)

            # 5) create another copy of that buildcache on "local artifact
            # mirror" (if enabled)
            if enable_artifacts_mirror:
                tty.msg('Creating local artifact buildcache in {0}'.format(
                    artifact_mirror_url))
                buildcache._createtarball(
                    env, job_spec_yaml_path, None, artifact_mirror_url, None,
                    True, True, False, False, True, False)

                if enable_cdash:
                    tty.msg('Writing .cdashid ({0}) to artifacts ({1})'.format(
                        cdash_build_id, artifact_mirror_url))
                    spack_ci.write_cdashid_to_mirror(
                        cdash_build_id, job_spec, artifact_mirror_url)

            # 6) relate this build to its dependencies on CDash (if enabled)
            if enable_cdash:
                mirror_url = remote_mirror_url
                if enable_artifacts_mirror:
                    mirror_url = artifact_mirror_url
                post_url = '{0}/api/v1/relateBuilds.php'.format(cdash_base_url)
                spack_ci.relate_cdash_builds(
                    spec_map, post_url, cdash_build_id, cdash_project,
                    mirror_url)
        else:
            # There is nothing to do here unless "local artifact mirror" is
            # enabled, in which case, we need to download the buildcache to
            # the local artifacts directory to be used by dependent jobs in
            # subsequent stages
            tty.msg('No need to rebuild {0}'.format(job_spec_pkg_name))
            if enable_artifacts_mirror:
                tty.msg('Getting buildcache for {0}'.format(job_spec_pkg_name))
                tty.msg('Downloading to {0}'.format(build_cache_dir))
                buildcache.download_buildcache_files(
                    job_spec, build_cache_dir, True, remote_mirror_url)


def ci_start(args):
    """Kicks of the CI process (currently just calls ci_generate() then
       ci_push())"""
    ci_generate(args)
    ci_pushyaml(args)


def ci(parser, args):
    if args.func:
        args.func(args)
