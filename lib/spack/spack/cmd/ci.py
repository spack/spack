# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile

from six.moves.urllib.parse import urlencode

import llnl.util.tty as tty

import spack.binary_distribution as bindist
import spack.ci as spack_ci
import spack.cmd.buildcache as buildcache
import spack.config as cfg
import spack.environment as ev
import spack.hash_types as ht
import spack.mirror
import spack.util.spack_yaml as syaml
import spack.util.url as url_util
import spack.util.web as web_util

description = "manage continuous integration pipelines"
section = "build"
level = "long"

CI_REBUILD_INSTALL_BASE_ARGS = ['spack', '-d', '-v']
INSTALL_FAIL_CODE = 1


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
        help="Path to file where generated jobs file should be " +
             "written.  The default is .gitlab-ci.yml in the root of the " +
             "repository.")
    generate.add_argument(
        '--copy-to', default=None,
        help="Absolute path of additional location where generated jobs " +
             "yaml file should be copied.  Default is not to copy.")
    generate.add_argument(
        '--optimize', action='store_true', default=False,
        help="(Experimental) run the generated document through a series of "
             "optimization passes designed to reduce the size of the "
             "generated file.")
    generate.add_argument(
        '--dependencies', action='store_true', default=False,
        help="(Experimental) disable DAG scheduling; use "
             ' "plain" dependencies.')
    generate.add_argument(
        '--buildcache-destination', default=None,
        help="Override the mirror configured in the environment (spack.yaml) " +
             "in order to push binaries from the generated pipeline to a " +
             "different location.")
    prune_group = generate.add_mutually_exclusive_group()
    prune_group.add_argument(
        '--prune-dag', action='store_true', dest='prune_dag',
        default=True, help="""Do not generate jobs for specs already up to
date on the mirror""")
    prune_group.add_argument(
        '--no-prune-dag', action='store_false', dest='prune_dag',
        default=True, help="""Generate jobs for specs already up to date
on the mirror""")
    generate.add_argument(
        '--check-index-only', action='store_true', dest='index_only',
        default=False, help="""Spack always check specs against configured
binary mirrors when generating the pipeline, regardless of whether or not
DAG pruning is enabled.  This flag controls whether it might attempt to
fetch remote spec files directly (ensuring no spec is rebuilt if it
is present on the mirror), or whether it should reduce pipeline generation time
by assuming all remote buildcache indices are up to date and only use those
to determine whether a given spec is up to date on mirrors.  In the latter
case, specs might be needlessly rebuilt if remote buildcache indices are out
of date.""")
    generate.add_argument(
        '--artifacts-root', default=None,
        help="""Path to root of artifacts directory.  If provided, concrete
environment files (spack.yaml, spack.lock) will be generated under this
path and their location sent to generated child jobs via the custom job
variable SPACK_CONCRETE_ENVIRONMENT_PATH.""")
    generate.set_defaults(func=ci_generate)

    # Rebuild the buildcache index associated with the mirror in the
    # active, gitlab-enabled environment.
    index = subparsers.add_parser('rebuild-index', help=ci_reindex.__doc__)
    index.set_defaults(func=ci_reindex)

    # Handle steps of a ci build/rebuild
    rebuild = subparsers.add_parser('rebuild', help=ci_rebuild.__doc__)
    rebuild.set_defaults(func=ci_rebuild)

    # Facilitate reproduction of a failed CI build job
    reproduce = subparsers.add_parser('reproduce-build',
                                      help=ci_reproduce.__doc__)
    reproduce.add_argument('job_url', help='Url of job artifacts bundle')
    reproduce.add_argument('--working-dir', help="Where to unpack artifacts",
                           default=os.path.join(os.getcwd(), 'ci_reproduction'))

    reproduce.set_defaults(func=ci_reproduce)


def ci_generate(args):
    """Generate jobs file from a spack environment file containing CI info.
       Before invoking this command, you can set the environment variable
       SPACK_CDASH_AUTH_TOKEN to contain the CDash authorization token
       for creating a build group for the generated workload and registering
       all generated jobs under that build group.  If this environment
       variable is not set, no build group will be created on CDash."""
    env = spack.cmd.require_active_env(cmd_name='ci generate')

    output_file = args.output_file
    copy_yaml_to = args.copy_to
    run_optimizer = args.optimize
    use_dependencies = args.dependencies
    prune_dag = args.prune_dag
    index_only = args.index_only
    artifacts_root = args.artifacts_root
    buildcache_destination = args.buildcache_destination

    if not output_file:
        output_file = os.path.abspath(".gitlab-ci.yml")
    else:
        output_file_path = os.path.abspath(output_file)
        gen_ci_dir = os.path.dirname(output_file_path)
        if not os.path.exists(gen_ci_dir):
            os.makedirs(gen_ci_dir)

    # Generate the jobs
    spack_ci.generate_gitlab_ci_yaml(
        env, True, output_file, prune_dag=prune_dag,
        check_index_only=index_only, run_optimizer=run_optimizer,
        use_dependencies=use_dependencies, artifacts_root=artifacts_root,
        remote_mirror_override=buildcache_destination)

    if copy_yaml_to:
        copy_to_dir = os.path.dirname(copy_yaml_to)
        if not os.path.exists(copy_to_dir):
            os.makedirs(copy_to_dir)
        shutil.copyfile(output_file, copy_yaml_to)


def ci_reindex(args):
    """Rebuild the buildcache index associated with the mirror in the
       active, gitlab-enabled environment. """
    env = spack.cmd.require_active_env(cmd_name='ci rebuild-index')
    yaml_root = ev.config_dict(env.yaml)

    if 'mirrors' not in yaml_root or len(yaml_root['mirrors'].values()) < 1:
        tty.die('spack ci rebuild-index requires an env containing a mirror')

    ci_mirrors = yaml_root['mirrors']
    mirror_urls = [url for url in ci_mirrors.values()]
    remote_mirror_url = mirror_urls[0]

    buildcache.update_index(remote_mirror_url, update_keys=True)


def ci_rebuild(args):
    """Check a single spec against the remote mirror, and rebuild it from
       source if the mirror does not contain the full hash match of the spec
       as computed locally. """
    env = spack.cmd.require_active_env(cmd_name='ci rebuild')

    # Make sure the environment is "gitlab-enabled", or else there's nothing
    # to do.
    yaml_root = ev.config_dict(env.yaml)
    gitlab_ci = None
    if 'gitlab-ci' in yaml_root:
        gitlab_ci = yaml_root['gitlab-ci']

    if not gitlab_ci:
        tty.die('spack ci rebuild requires an env containing gitlab-ci cfg')

    tty.msg('SPACK_BUILDCACHE_DESTINATION={0}'.format(os.environ.get('SPACK_BUILDCACHE_DESTINATION', None)))

    # Grab the environment variables we need.  These either come from the
    # pipeline generation step ("spack ci generate"), where they were written
    # out as variables, or else provided by GitLab itself.
    pipeline_artifacts_dir = get_env_var('SPACK_ARTIFACTS_ROOT')
    job_log_dir = get_env_var('SPACK_JOB_LOG_DIR')
    repro_dir = get_env_var('SPACK_JOB_REPRO_DIR')
    local_mirror_dir = get_env_var('SPACK_LOCAL_MIRROR_DIR')
    concrete_env_dir = get_env_var('SPACK_CONCRETE_ENV_DIR')
    ci_pipeline_id = get_env_var('CI_PIPELINE_ID')
    ci_job_name = get_env_var('CI_JOB_NAME')
    signing_key = get_env_var('SPACK_SIGNING_KEY')
    root_spec = get_env_var('SPACK_ROOT_SPEC')
    job_spec_pkg_name = get_env_var('SPACK_JOB_SPEC_PKG_NAME')
    compiler_action = get_env_var('SPACK_COMPILER_ACTION')
    cdash_build_name = get_env_var('SPACK_CDASH_BUILD_NAME')
    spack_pipeline_type = get_env_var('SPACK_PIPELINE_TYPE')
    remote_mirror_override = get_env_var('SPACK_REMOTE_MIRROR_OVERRIDE')
    remote_mirror_url = get_env_var('SPACK_REMOTE_MIRROR_URL')

    # Construct absolute paths relative to current $CI_PROJECT_DIR
    ci_project_dir = get_env_var('CI_PROJECT_DIR')
    pipeline_artifacts_dir = os.path.join(
        ci_project_dir, pipeline_artifacts_dir)
    job_log_dir = os.path.join(ci_project_dir, job_log_dir)
    repro_dir = os.path.join(ci_project_dir, repro_dir)
    local_mirror_dir = os.path.join(ci_project_dir, local_mirror_dir)
    concrete_env_dir = os.path.join(ci_project_dir, concrete_env_dir)

    # Debug print some of the key environment variables we should have received
    tty.debug('pipeline_artifacts_dir = {0}'.format(pipeline_artifacts_dir))
    tty.debug('root_spec = {0}'.format(root_spec))
    tty.debug('remote_mirror_url = {0}'.format(remote_mirror_url))
    tty.debug('job_spec_pkg_name = {0}'.format(job_spec_pkg_name))
    tty.debug('compiler_action = {0}'.format(compiler_action))

    # Query the environment manifest to find out whether we're reporting to a
    # CDash instance, and if so, gather some information from the manifest to
    # support that task.
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
        tty.debug('job_spec_buildgroup = {0}'.format(job_spec_buildgroup))

    # Is this a pipeline run on a spack PR or a merge to develop?  It might
    # be neither, e.g. a pipeline run on some environment repository.
    spack_is_pr_pipeline = spack_pipeline_type == 'spack_pull_request'
    spack_is_develop_pipeline = spack_pipeline_type == 'spack_protected_branch'

    tty.debug('Pipeline type - PR: {0}, develop: {1}'.format(
        spack_is_pr_pipeline, spack_is_develop_pipeline))

    # If no override url exists, then just push binary package to the
    # normal remote mirror url.
    buildcache_mirror_url = remote_mirror_override or remote_mirror_url

    # Figure out what is our temporary storage mirror: Is it artifacts
    # buildcache?  Or temporary-storage-url-prefix?  In some cases we need to
    # force something or pipelines might not have a way to propagate build
    # artifacts from upstream to downstream jobs.
    pipeline_mirror_url = None

    temp_storage_url_prefix = None
    if 'temporary-storage-url-prefix' in gitlab_ci:
        temp_storage_url_prefix = gitlab_ci['temporary-storage-url-prefix']
        pipeline_mirror_url = url_util.join(
            temp_storage_url_prefix, ci_pipeline_id)

    enable_artifacts_mirror = False
    if 'enable-artifacts-buildcache' in gitlab_ci:
        enable_artifacts_mirror = gitlab_ci['enable-artifacts-buildcache']
        if (enable_artifacts_mirror or (spack_is_pr_pipeline and
            not enable_artifacts_mirror and not temp_storage_url_prefix)):
            # If you explicitly enabled the artifacts buildcache feature, or
            # if this is a PR pipeline but you did not enable either of the
            # per-pipeline temporary storage features, we force the use of
            # artifacts buildcache.  Otherwise jobs will not have binary
            # dependencies from previous stages available since we do not
            # allow pushing binaries to the remote mirror during PR pipelines.
            enable_artifacts_mirror = True
            pipeline_mirror_url = 'file://' + local_mirror_dir
            mirror_msg = 'artifact buildcache enabled, mirror url: {0}'.format(
                pipeline_mirror_url)
            tty.debug(mirror_msg)

    # Whatever form of root_spec we got, use it to get a map giving us concrete
    # specs for this job and all of its dependencies.
    spec_map = spack_ci.get_concrete_specs(
        env, root_spec, job_spec_pkg_name, compiler_action)
    job_spec = spec_map[job_spec_pkg_name]

    job_spec_yaml_file = '{0}.yaml'.format(job_spec_pkg_name)
    job_spec_yaml_path = os.path.join(repro_dir, job_spec_yaml_file)

    # To provide logs, cdash reports, etc for developer download/perusal,
    # these things have to be put into artifacts.  This means downstream
    # jobs that "need" this job will get those artifacts too.  So here we
    # need to clean out the artifacts we may have got from upstream jobs.

    cdash_report_dir = os.path.join(pipeline_artifacts_dir, 'cdash_report')
    if os.path.exists(cdash_report_dir):
        shutil.rmtree(cdash_report_dir)

    if os.path.exists(job_log_dir):
        shutil.rmtree(job_log_dir)

    if os.path.exists(repro_dir):
        shutil.rmtree(repro_dir)

    # Now that we removed them if they existed, create the directories we
    # need for storing artifacts.  The cdash_report directory will be
    # created internally if needed.
    os.makedirs(job_log_dir)
    os.makedirs(repro_dir)

    # Copy the concrete environment files to the repro directory so we can
    # expose them as artifacts and not conflict with the concrete environment
    # files we got as artifacts from the upstream pipeline generation job.
    # Try to cast a slightly wider net too, and hopefully get the generated
    # pipeline yaml.  If we miss it, the user will still be able to go to the
    # pipeline generation job and get it from there.
    target_dirs = [
        concrete_env_dir,
        pipeline_artifacts_dir
    ]

    for dir_to_list in target_dirs:
        for file_name in os.listdir(dir_to_list):
            src_file = os.path.join(dir_to_list, file_name)
            if os.path.isfile(src_file):
                dst_file = os.path.join(repro_dir, file_name)
                shutil.copyfile(src_file, dst_file)

    # If signing key was provided via "SPACK_SIGNING_KEY", then try to
    # import it.
    if signing_key:
        spack_ci.import_signing_key(signing_key)

    # Depending on the specifics of this job, we might need to turn on the
    # "config:install_missing compilers" option (to build this job spec
    # with a bootstrapped compiler), or possibly run "spack compiler find"
    # (to build a bootstrap compiler or one of its deps in a
    # compiler-agnostic way), or maybe do nothing at all (to build a spec
    # using a compiler already installed on the target system).
    spack_ci.configure_compilers(compiler_action)

    # Write this job's spec yaml into the reproduction directory, and it will
    # also be used in the generated "spack install" command to install the spec
    tty.debug('job concrete spec path: {0}'.format(job_spec_yaml_path))
    with open(job_spec_yaml_path, 'w') as fd:
        fd.write(job_spec.to_yaml(hash=ht.build_hash))

    # Write the concrete root spec yaml into the reproduction directory
    root_spec_yaml_path = os.path.join(repro_dir, 'root.yaml')
    with open(root_spec_yaml_path, 'w') as fd:
        fd.write(spec_map['root'].to_yaml(hash=ht.build_hash))

    # Write some other details to aid in reproduction into an artifact
    repro_file = os.path.join(repro_dir, 'repro.json')
    repro_details = {
        'job_name': ci_job_name,
        'job_spec_yaml': job_spec_yaml_file,
        'root_spec_yaml': 'root.yaml',
        'ci_project_dir': ci_project_dir
    }
    with open(repro_file, 'w') as fd:
        fd.write(json.dumps(repro_details))

    # Write information about spack into an artifact in the repro dir
    spack_info = spack_ci.get_spack_info()
    spack_info_file = os.path.join(repro_dir, 'spack_info.txt')
    with open(spack_info_file, 'wb') as fd:
        fd.write(b'\n')
        fd.write(spack_info.encode('utf8'))
        fd.write(b'\n')

    # If we decided there should be a temporary storage mechanism, add that
    # mirror now so it's used when we check for a full hash match already
    # built for this spec.
    if pipeline_mirror_url:
        spack.mirror.add(spack_ci.TEMP_STORAGE_MIRROR_NAME,
                         pipeline_mirror_url,
                         cfg.default_modify_scope())

    # Check configured mirrors for a built spec with a matching full hash
    matches = bindist.get_mirrors_for_spec(
        job_spec, full_hash_match=True, index_only=False)

    if matches:
        # Got a full hash match on at least one configured mirror.  All
        # matches represent the fully up-to-date spec, so should all be
        # equivalent.  If artifacts mirror is enabled, we just pick one
        # of the matches and download the buildcache files from there to
        # the artifacts, so they're available to be used by dependent
        # jobs in subsequent stages.
        tty.msg('No need to rebuild {0}, found full hash match at: '.format(
            job_spec_pkg_name))
        for match in matches:
            tty.msg('    {0}'.format(match['mirror_url']))
        if enable_artifacts_mirror:
            matching_mirror = matches[0]['mirror_url']
            build_cache_dir = os.path.join(local_mirror_dir, 'build_cache')
            tty.debug('Getting {0} buildcache from {1}'.format(
                job_spec_pkg_name, matching_mirror))
            tty.debug('Downloading to {0}'.format(build_cache_dir))
            bindist.download_single_spec(
                job_spec,
                build_cache_dir,
                mirror_url=matching_mirror
            )

        # Now we are done and successful
        sys.exit(0)

    # No full hash match anywhere means we need to rebuild spec

    # Start with spack arguments
    install_args = [base_arg for base_arg in CI_REBUILD_INSTALL_BASE_ARGS]

    config = cfg.get('config')
    if not config['verify_ssl']:
        install_args.append('-k')

    install_args.extend([
        'install',
        '--keep-stage',
        '--require-full-hash-match',
    ])

    can_verify = spack_ci.can_verify_binaries()
    verify_binaries = can_verify and spack_is_pr_pipeline is False
    if not verify_binaries:
        install_args.append('--no-check-signature')

    if enable_cdash:
        # Add additional arguments to `spack install` for CDash reporting.
        cdash_upload_url = '{0}/submit.php?project={1}'.format(
            cdash_base_url, cdash_project_enc)

        install_args.extend([
            '--cdash-upload-url', cdash_upload_url,
            '--cdash-build', cdash_build_name,
            '--cdash-site', cdash_site,
            '--cdash-track', job_spec_buildgroup,
        ])

    # A compiler action of 'FIND_ANY' means we are building a bootstrap
    # compiler or one of its deps.
    # TODO: when compilers are dependencies, we should include --no-add
    if compiler_action != 'FIND_ANY':
        install_args.append('--no-add')

    # TODO: once we have the concrete spec registry, use the DAG hash
    # to identify the spec to install, rather than the concrete spec
    # yaml file.
    install_args.extend(['-f', job_spec_yaml_path])

    tty.debug('Installing {0} from source'.format(job_spec.name))
    tty.debug('spack install arguments: {0}'.format(
        install_args))

    # Write the install command to a shell script
    with open('install.sh', 'w') as fd:
        fd.write('#!/bin/bash\n\n')
        fd.write('\n# spack install command\n')
        fd.write(' '.join(['"{0}"'.format(i) for i in install_args]))
        fd.write('\n')

    st = os.stat('install.sh')
    os.chmod('install.sh', st.st_mode | stat.S_IEXEC)

    install_copy_path = os.path.join(repro_dir, 'install.sh')
    shutil.copyfile('install.sh', install_copy_path)

    # Run the generated install.sh shell script as if it were being run in
    # a login shell.
    try:
        install_process  = subprocess.Popen(['bash', '-l', './install.sh'])
        install_process.wait()
        install_exit_code = install_process.returncode
    except (ValueError, subprocess.CalledProcessError, OSError) as inst:
        tty.error('Encountered error running install script')
        tty.error(inst)

    # Now do the post-install tasks
    tty.debug('spack install exited {0}'.format(install_exit_code))

    # If a spec fails to build in a spack develop pipeline, we add it to a
    # list of known broken full hashes.  This allows spack PR pipelines to
    # avoid wasting compute cycles attempting to build those hashes.
    if install_exit_code == INSTALL_FAIL_CODE and spack_is_develop_pipeline:
        tty.debug('Install failed on develop')
        if 'broken-specs-url' in gitlab_ci:
            broken_specs_url = gitlab_ci['broken-specs-url']
            dev_fail_hash = job_spec.full_hash()
            broken_spec_path = url_util.join(broken_specs_url, dev_fail_hash)
            tty.msg('Reporting broken develop build as: {0}'.format(
                broken_spec_path))
            tmpdir = tempfile.mkdtemp()
            empty_file_path = os.path.join(tmpdir, 'empty.txt')

            broken_spec_details = {
                'broken-spec': {
                    'job-url': get_env_var('CI_JOB_URL'),
                    'pipeline-url': get_env_var('CI_PIPELINE_URL'),
                    'concrete-spec-yaml': job_spec.to_dict(hash=ht.full_hash)
                }
            }

            try:
                with open(empty_file_path, 'w') as efd:
                    efd.write(syaml.dump(broken_spec_details))
                web_util.push_to_url(
                    empty_file_path,
                    broken_spec_path,
                    keep_original=False,
                    extra_args={'ContentType': 'text/plain'})
            except Exception as err:
                # If we got some kind of S3 (access denied or other connection
                # error), the first non boto-specific class in the exception
                # hierarchy is Exception.  Just print a warning and return
                msg = 'Error writing to broken specs list {0}: {1}'.format(
                    broken_spec_path, err)
                tty.warn(msg)
            finally:
                shutil.rmtree(tmpdir)

    # We generated the "spack install ..." command to "--keep-stage", copy
    # any logs from the staging directory to artifacts now
    spack_ci.copy_stage_logs_to_artifacts(job_spec, job_log_dir)

    # If the install succeeded, create a buildcache entry for this job spec
    # and push it to one or more mirrors.  If the install did not succeed,
    # print out some instructions on how to reproduce this build failure
    # outside of the pipeline environment.
    if install_exit_code == 0:
        can_sign = spack_ci.can_sign_binaries()
        sign_binaries = can_sign and spack_is_pr_pipeline is False

        # Create buildcache in either the main remote mirror, or in the
        # per-PR mirror, if this is a PR pipeline
        if buildcache_mirror_url:
            spack_ci.push_mirror_contents(
                env, job_spec_yaml_path, buildcache_mirror_url, sign_binaries
            )

        # Create another copy of that buildcache in the per-pipeline
        # temporary storage mirror (this is only done if either
        # artifacts buildcache is enabled or a temporary storage url
        # prefix is set)
        if pipeline_mirror_url:
            spack_ci.push_mirror_contents(
                env, job_spec_yaml_path, pipeline_mirror_url, sign_binaries
            )

        # If this is a develop pipeline, check if the spec that we just built is
        # on the broken-specs list. If so, remove it.
        if spack_is_develop_pipeline and 'broken-specs-url' in gitlab_ci:
            broken_specs_url = gitlab_ci['broken-specs-url']
            just_built_hash = job_spec.full_hash()
            broken_spec_path = url_util.join(broken_specs_url, just_built_hash)
            if web_util.url_exists(broken_spec_path):
                tty.msg('Removing {0} from the list of broken specs'.format(
                    broken_spec_path))
                try:
                    web_util.remove_url(broken_spec_path)
                except Exception as err:
                    # If we got some kind of S3 (access denied or other connection
                    # error), the first non boto-specific class in the exception
                    # hierarchy is Exception.  Just print a warning and return
                    msg = 'Error removing {0} from broken specs list: {1}'.format(
                        broken_spec_path, err)
                    tty.warn(msg)

    else:
        tty.debug('spack install exited non-zero, will not create buildcache')

        api_root_url = get_env_var('CI_API_V4_URL')
        ci_project_id = get_env_var('CI_PROJECT_ID')
        ci_job_id = get_env_var('CI_JOB_ID')

        repro_job_url = '{0}/projects/{1}/jobs/{2}/artifacts'.format(
            api_root_url, ci_project_id, ci_job_id)

        # Control characters cause this to be printed in blue so it stands out
        reproduce_msg = """

\033[34mTo reproduce this build locally, run:

    spack ci reproduce-build {0} [--working-dir <dir>]

If this project does not have public pipelines, you will need to first:

    export GITLAB_PRIVATE_TOKEN=<generated_token>

... then follow the printed instructions.\033[0;0m

""".format(repro_job_url)

        print(reproduce_msg)

    # Tie job success/failure to the success/failure of building the spec
    return install_exit_code


def ci_reproduce(args):
    job_url = args.job_url
    work_dir = args.working_dir

    return spack_ci.reproduce_ci_job(job_url, work_dir)


def ci(parser, args):
    if args.func:
        return args.func(args)
