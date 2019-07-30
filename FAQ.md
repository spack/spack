# FAQ for BBP spack usage


<details>
  <summary>Q: How do I build and *load* a piece of software?</summary>

  We'll install `Ed(1)`, the standard editor.

  Make sure you're setup as per [this](https://github.com/BlueBrain/spack#building-software-on-bluebrain5).

  Specifically that you have the `spack` git repo on the `develop` branch,
  and have created and linked the files into `~/.spack/`

  ```console
  spack install ed
  ```

  This produces output, and should end with something like:
  `$SPACK_INSTALL_PREFIX/linux-rhel7-x86_64/gcc-6.4.0/ed-1.4-35jlkv`

  One can then run `ed` with
  ```
  $SPACK_INSTALL_PREFIX/linux-rhel7-x86_64/gcc-6.4.0/ed-1.4-35jlkv/ed
  ```

  More complex packages will have an environment that needs to be setup by
  the module system.
  To find the module that was built, issue:
  ```
  spack module tcl find --full-path ed
  ```

  At which point, you should be able to:
  ```
  module load $path_from_above
  ```
</details>

<details>
  <summary>Q: How do I add/update my package/module versions?</summary>

  We want to add a new version 2.0.0 to `mypackage`.

  Make sure you're setup as per [the instructions](https://github.com/BlueBrain/spack#building-software-on-bluebrain5).

  Change your package recipe to add or update the version specifying the 
  correspondant tag or commit.
  
  ```
  spack edit mypackage
  ...
  version('2.0.0', tag='v2.0.0')
  ...
  ```

  Then you can edit the packages yaml files depending on the type 
  of package (`bbp-packages.yaml`, `external-libraries.yaml`…).
  
  Assuming `mypackage` is an external library:
  ```
  vim deploy/packages/external-libraries.yaml
  ```

  Under the spec section
  ```
  - mypackage@2.0.0
  ```

  After that you should edit the module file that will be at 
  `deploy/config/external-libraries/`
  ```
  vim deploy/config/external-libraries/modules.yaml
  ```

  Under the whitelist section, ensure that your software is mentioned:
  ```
  - mypackage
  ```
  
  Now you are ready to create a new branch and a PR with the changes.
  You can check the Jenkins build of your PR [on Blue Ocean](https://bbpcode.epfl.ch/ci/blue/organizations/jenkins/hpc.spack-deployment/activity).
  
</details>

<details>
  <summary>Q: How do I test my modules from the PR?</summary>

  If you followed the previous point you should be able to see if your 
  PR was succesfully built [on Blue Ocean](https://bbpcode.epfl.ch/ci/blue/organizations/jenkins/hpc.spack-deployment/activity).

  Then you can log into `BB5` and run the following commands:
  ```
  module purge
  unset MODULEPATH
  source /gpfs/bbp.cscs.ch/apps/hpc/jenkins/pulls/xxx/config/modules.sh
  ```
  Where `xxx` is the number of your PR.

  At this point you should have the environment ready, so if your module 
  was built correctly you should be able to load it.
  ```
  module load mypackage
  ```

  Now you are ready to test `mypackage`

</details>

<details>
  <summary>Q: Why do I have to rebuild the entire world?</summary>

  If you are on the `BB5`, you shouldn't need to.

  As [described here](https://github.com/BlueBrain/spack#building-software-on-bluebrain5),
  one can use the system packages available with an appropriate
  `~/.spack/packages.yaml` and `~/.spack/upstreams.yaml`.
</details>

<details>
  <summary>Q: Why do I see <code>PACK_INSTALL_PREFIX</code> in my install?  Things are failing!</summary>

  It is expected that the environment variable `$SPACK_INSTALL_PREFIX` is defined.
  If it isn't you, may be getting weird expansions from that.
</details>

<details>
  <summary>Q: Why are the module files not being rebuilt?</summary>

  The `spack module tcl refresh` command respects a blacklists that are in:
  * `~/.spack/modules.yaml`

  Examples from our deployment workflow can be found in:
  * `spack/deploy/configs/applications/modules.yaml`
  * `spack/deploy/configs/serial-libraries/modules.yaml`

  Run `spack --debug module tcl refresh` and search for the module you
  expect to be built.
  Modify the blacklist to have the module built.
</details>

<details>
  <summary>Q: Why is it so slow to interact with the `spack` repository if on GPFS</summary>

  Make sure the `spack` repo is checked out in a subdirectory of `$HOME`.
  The `spack` repository is quite large, and when it is checked out under a
  `/gpfs/bbp.cscs.ch/project/*` directory, performance can be 10x slower
  than on the SSD provided storage of `$HOME`.
</details>

<details>
  <summary>Q: Is there a binary cache?</summary>

  We currently have a binary cache for central deployment only. As
  universally relocatable binaries are very fragile, we do not support
  binary caches for end-users.

  Please make sure you have setup the correct configurations in:
  * `~/.spack/packages.yaml`
  * `~/.spack/upstreams.yaml`
  to avoid rebuilding packages that have already been build centrally.
</details>

<details>
  <summary>Q: How do I debug my Pull Request?</summary>

  To re-create the environment a Pull Request was built in, let's say #666,
  and debug failures, it is recommended to create a throw-away shell
  environment and execute the following commands.  Note that the parameters
  in the first line correspond to the pull request and the stage you wish
  to debug (as labelled in Jenkins, but lowercase):
  ```console
  eval $(${SPACK_ROOT}/deploy/pull_env.sh pulls/666 applications)
  spacktivate
  spack install $(grep <my_failed_piece_of_software> ${HOME}/specs.txt)
  ```
  Evaluating the first line will override local environment variables such
  as the current `$HOME` directory.  *After leaving the shell, this will
  leave a temporary directory behind*, following the pattern `spack_*`.
  Please make sure to delete this directory when not needed any longer.
</details>
