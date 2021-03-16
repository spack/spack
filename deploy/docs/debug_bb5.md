# Debugging pull requests on BlueBrain5

If a pull request against the current state of the deployment fails, e.g.,
during concretization, the following steps may help debug issues.

1. Check out the pull request in your local Spack setup and set some
   references to the failed stage of the deployment and the pull request
   number:
   ```console
   export PR_NUMBER=1234
   export PR_STAGE=applications
   export PR_BASE=$(readlink -f /gpfs/bbp.cscs.ch/ssd/apps/hpc/jenkins/pulls/${PR_NUMBER}/deploy/${PR_STAGE}/latest)
   ```
2. Move your own configuration files out of the way. If the official
   instructions are following, one can use:
   ```console
   for fn in ${SPACK_ROOT}/etc/spack/*.yaml; do mv ${fn}{,.old}; done
   ```
3. Copy the environment that the CI is attempting to build somewhere under
   your control:
   ```console
   cp -R ${PR_BASE}/data/build_environment .
   ```
   If the concretization of the build environment fails, it is easier to
   re-use the installation directory of the CI for packages that have been
   built already:
   ```console
   export SPACK_INSTALL_PREFIX=${PR_BASE}
   ```
   Otherwise, for build issues, the above will not work due to the required
   write permissions.
   Create a new installation directory instead:
   ```console
   export SPACK_INSTALL_PREFIX=${PWD}/build_environment/install
   ```
4. Run the concretization, using the configuration of the CI:
   ```console
   spack -C ${PR_BASE}/data/.spack -D build_environment concretize -f
   ```
5. Fix any issue arising, re-iterate starting from 4.
6. Clean everything up:
   ```console
   rm -rf build_environment
   for fn in ${SPACK_ROOT}/etc/spack/*.yaml.old; do mv ${fn} ${fn%%.old}; done
   ```
