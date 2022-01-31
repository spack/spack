# Debugging pull requests on BlueBrain5

## Build failures

Build failures should be found under the tab "Tests" in the GitLab pipeline
interface that is linked from the GitHub pull request.

Future changes to the deployment may list build failures directly and/or
include build logs.

## Concretization failures

If a pull request against the current state of the deployment fails
during concretization, the following steps may help debug issues.

1. Check out the pull request in your local Spack setup,
   and make sure that you sourced your local Spack clone.

   Then unset or reset any variables that may interfere with the PR building:
   ```console
   unset SPACK_SYSTEM_CONFIG_PATH
   export SPACK_USER_CACHE_PATH=/tmp/debug_spack_pr_$(whoami)_cache
   ```
2. Note the job that is failing, i.e., `libraries` in the `applications`
   stage, with id `140355`.

   Copy its configuration to different location and use it:
   ```console
   export SPACK_USER_CONFIG_PATH=/tmp/debug_spack_pr_$(whoami)_config

   export FAILED_JOB=140355
   export STUB=/gpfs/bbp.cscs.ch/ssd/gitlab_map_jobs/bbpcihpcdeploy
   cp -r ${STUB}/J${FAILED_JOB}/hpc/spack/spack_config ${SPACK_USER_CONFIG_PATH}
   ```
   Then set the installation directory to a temporary writable one:
   ```console
   spack config add config:install_tree:root:/tmp/debug_spack_pr_$(whoami)_software
   spack config add config:module_roots:tcl:/tmp/debug_spack_pr_$(whoami)_modules
   ```
3. Recreate the environment used to build in the CI and activate it.
   Recall that `applications` was failing in `libraries`:
   ```console
   spack env create pr_debug ${SPACK_ROOT}/bluebrain/deployment/environments/applications_libraries.yaml
   spack env activate pr_debug
   ```
4. Trigger the concretization:
   ```console
   spack concretize -f
   ```
5. If debugging a build is desired, install the environment:
   ```console
   spack install
   ```
6. Fix any issue arising, re-iterate starting from 4.
   [The FAQ may help](FAQ.md#concretization-issues) with debugging certain
   issues.
8. Clean everything up:
   ```console
   rm -r /tmp/debug_spack_pr_$(whoami)_cache
   rm -r /tmp/debug_spack_pr_$(whoami)_config
   rm -r /tmp/debug_spack_pr_$(whoami)_modules
   rm -r /tmp/debug_spack_pr_$(whoami)_software
   ```
   Finally, to ensure a clean reset of your shell environment, close your SSH connection to BlueBrain5.
