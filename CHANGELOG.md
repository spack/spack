# v0.19.1 (2023-02-07)

### Spack Bugfixes

* `buildcache create`: make "file exists" less verbose (#35019)
* `spack mirror create`: don't change paths to urls (#34992)
* Improve error message for requirements (#33988)
* uninstall: fix accidental cubic complexity (#34005)
* scons: fix signature for `install_args` (#34481)
* Fix `combine_phase_logs` text encoding issues (#34657)
* Use a module-like object to propagate changes in the MRO, when setting build env (#34059)
* PackageBase should not define builder legacy attributes (#33942)
* Forward lookup of the "run_tests" attribute (#34531)
* Bugfix for timers (#33917, #33900)
* Fix path handling in prefix inspections (#35318)
* Fix libtool filter for Fujitsu compilers (#34916)
* Bug fix for duplicate rpath errors on macOS when creating build caches (#34375)
* FileCache: delete the new cache file on exception (#34623)
* Propagate exceptions from Spack python console (#34547)
* Tests: Fix a bug/typo in a `config_values.py` fixture (#33886)
* Various CI fixes (#33953, #34560, #34560, #34828)
* Docs: remove monitors and analyzers, typos (#34358, #33926)
* bump release version for tutorial command (#33859)


# v0.19.0 (2022-11-11)

`v0.19.0` is a major feature release.

## Major features in this release

1. **Package requirements**

   Spack's traditional [package preferences](
     https://spack.readthedocs.io/en/latest/build_settings.html#package-preferences)
   are soft, but we've added hard requriements to `packages.yaml` and `spack.yaml`
   (#32528, #32369). Package requirements use the same syntax as specs:

   ```yaml
   packages:
     libfabric:
       require: "@1.13.2"
     mpich:
       require:
       - one_of: ["+cuda", "+rocm"]
   ```

   More details in [the docs](
     https://spack.readthedocs.io/en/latest/build_settings.html#package-requirements).

2. **Environment UI Improvements**

   * Fewer surprising modifications to `spack.yaml` (#33711):

     * `spack install` in an environment will no longer add to the `specs:` list; you'll
       need to either use `spack add <spec>` or `spack install --add <spec>`.

     * Similarly, `spack uninstall` will not remove from your environment's `specs:`
       list; you'll need to use `spack remove` or `spack uninstall --remove`.

     This will make it easier to manage an environment, as there is clear separation
     between the stack to be installed (`spack.yaml`/`spack.lock`) and which parts of
     it should be installed (`spack install` / `spack uninstall`).

   * `concretizer:unify:true` is now the default mode for new environments (#31787)

     We see more users creating `unify:true` environments now. Users who need
     `unify:false` can add it to their environment to get the old behavior. This will
     concretize every spec in the environment independently.

   * Include environment configuration from URLs (#29026, [docs](
       https://spack.readthedocs.io/en/latest/environments.html#included-configurations))

     You can now include configuration in your environment directly from a URL:

     ```yaml
     spack:
       include:
       - https://github.com/path/to/raw/config/compilers.yaml
     ```

4. **Multiple Build Systems**

   An increasing number of packages in the ecosystem need the ability to support
   multiple build systems (#30738, [docs](
     https://spack.readthedocs.io/en/latest/packaging_guide.html#multiple-build-systems)),
   either across versions, across platforms, or within the same version of the software.
   This has been hard to support through multiple inheritance, as methods from different
   build system superclasses would conflict. `package.py` files can now define separate
   builder classes with installation logic for different build systems, e.g.:

   ```python
   class ArpackNg(CMakePackage, AutotoolsPackage):

       build_system(
           conditional("cmake", when="@0.64:"),
           conditional("autotools", when="@:0.63"),
           default="cmake",
       )

   class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
       def cmake_args(self):
           pass

   class Autotoolsbuilder(spack.build_systems.autotools.AutotoolsBuilder):
       def configure_args(self):
           pass
   ```

5. **Compiler and variant propagation**

   Currently, compiler flags and variants are inconsistent: compiler flags set for a
   package are inherited by its dependencies, while variants are not. We should have
   these be consistent by allowing for inheritance to be enabled or disabled for both
   variants and compiler flags.

   Example syntax:
   - `package ++variant`:
         enabled variant that will be propagated to dependencies
   - `package +variant`:
         enabled variant that will NOT be propagated to dependencies
   - `package ~~variant`:
         disabled variant that will be propagated to dependencies
   - `package ~variant`:
         disabled variant that will NOT be propagated to dependencies
   - `package cflags==-g`:
         `cflags` will be propagated to dependencies
   - `package cflags=-g`:
         `cflags` will NOT be propagated to dependencies

   Syntax for non-boolan variants is similar to compiler flags. More in the docs for
   [variants](
     https://spack.readthedocs.io/en/latest/basic_usage.html#variants) and [compiler flags](
     https://spack.readthedocs.io/en/latest/basic_usage.html#compiler-flags).

6. **Enhancements to git version specifiers**

   * `v0.18.0` added the ability to use git commits as versions. You can now use the
     `git.` prefix to specify git tags or branches as versions. All of these are valid git
     versions in `v0.19` (#31200):

     ```console
     foo@abcdef1234abcdef1234abcdef1234abcdef1234      # raw commit
     foo@git.abcdef1234abcdef1234abcdef1234abcdef1234  # commit with git prefix
     foo@git.develop                                   # the develop branch
     foo@git.0.19                                      # use the 0.19 tag
     ```

   * `v0.19` also gives you more control over how Spack interprets git versions, in case
     Spack cannot detect the version from the git repository. You can suffix a git
     version with `=<version>` to force Spack to concretize it as a particular version
     (#30998, #31914, #32257):

     ```console
     # use mybranch, but treat it as version 3.2 for version comparison
     foo@git.mybranch=3.2

     # use the given commit, but treat it as develop for version comparison
     foo@git.abcdef1234abcdef1234abcdef1234abcdef1234=develop
     ```

     More in [the docs](
       https://spack.readthedocs.io/en/latest/basic_usage.html#version-specifier)

7. **Changes to Cray EX Support**

   Cray machines have historically had their own "platform" within Spack, because we
   needed to go through the module system to leverage compilers and MPI installations on
   these machines. The Cray EX programming environment now provides standalone `craycc`
   executables and proper `mpicc` wrappers, so Spack can treat EX machines like Linux
   with extra packages (#29392).

   We expect this to greatly reduce bugs, as external packages and compilers can now be
   used by prefix instead of through modules. We will also no longer be subject to
   reproducibility issues when modules change from Cray PE release to release and from
   site to site. This also simplifies dealing with the underlying Linux OS on cray
   systems, as Spack will properly model the machine's OS as either SuSE or RHEL.

8. **Improvements to tests and testing in CI**

   * `spack ci generate --tests` will generate a `.gitlab-ci.yml` file that not only does
     builds but also runs tests for built packages (#27877). Public GitHub pipelines now
     also run tests in CI.

   * `spack test run --explicit` will only run tests for packages that are explicitly
     installed, instead of all packages.

9. **Experimental binding link model**

   You can add a new option to `config.yaml` to make Spack embed absolute paths to
   needed shared libraries in ELF executables and shared libraries on Linux (#31948, [docs](
     https://spack.readthedocs.io/en/latest/config_yaml.html#shared-linking-bind)):

   ```yaml
   config:
     shared_linking:
       type: rpath
       bind: true
   ```

   This can improve launch time at scale for parallel applications, and it can make
   installations less susceptible to environment variables like `LD_LIBRARY_PATH`, even
   especially when dealing with external libraries that use `RUNPATH`. You can think of
   this as a faster, even higher-precedence version of `RPATH`.

## Other new features of note

* `spack spec` prints dependencies more legibly. Dependencies in the output now appear
  at the *earliest* level of indentation possible (#33406)
* You can override `package.py` attributes like `url`, directly in `packages.yaml`
  (#33275, [docs](
    https://spack.readthedocs.io/en/latest/build_settings.html#assigning-package-attributes))
* There are a number of new architecture-related format strings you can use in Spack
  configuration files to specify paths (#29810, [docs](
    https://spack.readthedocs.io/en/latest/configuration.html#config-file-variables))
* Spack now supports bootstrapping Clingo on Windows (#33400)
* There is now support for an `RPATH`-like library model on Windows (#31930)

## Performance Improvements

* Major performance improvements for installation from binary caches (#27610, #33628,
  #33636, #33608, #33590, #33496)
* Test suite can now be parallelized using `xdist` (used in GitHub Actions) (#32361)
* Reduce lock contention for parallel builds in environments (#31643)

## New binary caches and stacks

* We now build nearly all of E4S with `oneapi` in our buildcache (#31781, #31804,
  #31804, #31803, #31840, #31991, #32117, #32107, #32239)
* Added 3 new machine learning-centric stacks to binary cache: `x86_64_v3`, CUDA, ROCm
  (#31592, #33463)

## Removals and Deprecations

* Support for Python 3.5 is dropped (#31908). Only Python 2.7 and 3.6+ are officially
  supported.

* This is the last Spack release that will support Python 2 (#32615). Spack `v0.19`
  will emit a deprecation warning if you run it with Python 2, and Python 2 support will
  soon be removed from the `develop` branch.

* `LD_LIBRARY_PATH` is no longer set by default by `spack load` or module loads.

  Setting `LD_LIBRARY_PATH` in Spack environments/modules can cause binaries from
  outside of Spack to crash, and Spack's own builds use `RPATH` and do not need
  `LD_LIBRARY_PATH` set in order to run. If you still want the old behavior, you
  can run these commands to configure Spack to set `LD_LIBRARY_PATH`:

  ```console
  spack config add modules:prefix_inspections:lib64:[LD_LIBRARY_PATH]
  spack config add modules:prefix_inspections:lib:[LD_LIBRARY_PATH]
  ```

* The `spack:concretization:[together|separately]` has been removed after being
  deprecated in `v0.18`. Use `concretizer:unify:[true|false]`.
* `config:module_roots` is no longer supported after being deprecated in `v0.18`. Use
  configuration in module sets instead (#28659, [docs](
    https://spack.readthedocs.io/en/latest/module_file_support.html)).
* `spack activate` and `spack deactivate` are no longer supported, having been
  deprecated in `v0.18`. Use an environment with a view instead of
  activating/deactivating ([docs](
    https://spack.readthedocs.io/en/latest/environments.html#configuration-in-spack-yaml)).
* The old YAML format for buildcaches is now deprecated (#33707). If you are using an
  old buildcache with YAML metadata you will need to regenerate it with JSON metadata.
* `spack bootstrap trust` and `spack bootstrap untrust` are deprecated in favor of
  `spack bootstrap enable` and `spack bootstrap disable` and will be removed in `v0.20`.
  (#33600)
* The `graviton2` architecture has been renamed to `neoverse_n1`, and `graviton3`
  is now `neoverse_v1`. Buildcaches using the old architecture names will need to be rebuilt.
* The terms `blacklist` and `whitelist` have been replaced with `include` and `exclude`
  in all configuration files (#31569). You can use `spack config update` to
  automatically fix your configuration files.

## Notable Bugfixes

* Permission setting on installation now handles effective uid properly (#19980)
* `buildable:true` for an MPI implementation now overrides `buildable:false` for `mpi` (#18269)
* Improved error messages when attempting to use an unconfigured compiler (#32084)
* Do not punish explicitly requested compiler mismatches in the solver (#30074)
* `spack stage`: add missing --fresh and --reuse (#31626)
* Fixes for adding build system executables like `cmake` to package scope (#31739)
* Bugfix for binary relocation with aliased strings produced by newer `binutils` (#32253)

## Spack community stats

* 6,751 total packages, 335 new since `v0.18.0`
    * 141 new Python packages
    * 89 new R packages
* 303 people contributed to this release
    * 287 committers to packages
    * 57 committers to core


# v0.18.1 (2022-07-19)

### Spack Bugfixes
* Fix several bugs related to bootstrapping (#30834,#31042,#31180)
* Fix a regression that was causing spec hashes to differ between
  Python 2 and Python 3 (#31092)
* Fixed compiler flags for oneAPI and DPC++ (#30856)
* Fixed several issues related to concretization (#31142,#31153,#31170,#31226)
* Improved support for Cray manifest file and `spack external find` (#31144,#31201,#31173,#31186)
* Assign a version to openSUSE Tumbleweed according to the GLIBC version
  in the system (#19895)
* Improved Dockerfile generation for `spack containerize` (#29741,#31321)
* Fixed a few bugs related to concurrent execution of commands (#31509,#31493,#31477)

### Package updates
* WarpX: add v22.06, fixed libs property (#30866,#31102)
* openPMD: add v0.14.5, update recipe for @develop (#29484,#31023)

# v0.18.0 (2022-05-28)

`v0.18.0` is a major feature release.

## Major features in this release

1. **Concretizer now reuses by default**

   `spack install --reuse` was introduced in `v0.17.0`, and `--reuse`
   is now the default concretization mode. Spack will try hard to
   resolve dependencies using installed packages or binaries (#30396).

   To avoid reuse and to use the latest package configurations, (the
   old default), you can use `spack install --fresh`, or add
   configuration like this to your environment or `concretizer.yaml`:

   ```yaml
   concretizer:
       reuse: false
   ```

2. **Finer-grained hashes**

   Spack hashes now include `link`, `run`, *and* `build` dependencies,
   as well as a canonical hash of package recipes. Previously, hashes
   only included `link` and `run` dependencies (though `build`
   dependencies were stored by environments). We coarsened the hash to
   reduce churn in user installations, but the new default concretizer
   behavior mitigates this concern and gets us reuse *and* provenance.
   You will be able to see the build dependencies of new installations
   with `spack find`. Old installations will not change and their
   hashes will not be affected. (#28156, #28504, #30717, #30861)

3. **Improved error messages**

   Error handling with the new concretizer is now done with
   optimization criteria rather than with unsatisfiable cores, and
   Spack reports many more details about conflicting constraints.
   (#30669)

4. **Unify environments when possible**

   Environments have thus far supported `concretization: together` or
   `concretization: separately`. These have been replaced by a new
   preference in `concretizer.yaml`:

   ```yaml
   concretizer:
       unify: [true|false|when_possible]
   ```

   `concretizer:unify:when_possible` will *try* to resolve a fully
   unified environment, but if it cannot, it will create multiple
   configurations of some packages where it has to. For large
   environments that previously had to be concretized separately, this
   can result in a huge speedup (40-50x). (#28941)

5. **Automatically find externals on Cray machines**

   Spack can now automatically discover installed packages in the Cray
   Programming Environment by running `spack external find` (or `spack
   external read-cray-manifest` to *only* query the PE). Packages from
   the PE (e.g., `cray-mpich` are added to the database with full
   dependency information, and compilers from the PE are added to
   `compilers.yaml`. Available with the June 2022 release of the Cray
   Programming Environment. (#24894, #30428)

6. **New binary format and hardened signing**

   Spack now has an updated binary format, with improvements for
   security. The new format has a detached signature file, and Spack
   verifies the signature before untarring or decompressing the binary
   package. The previous format embedded the signature in a `tar`
   file, which required the client to run `tar` *before* verifying
   (#30750). Spack can still install from build caches using the old
   format, but we encourage users to switch to the new format going
   forward.

   Production GitLab pipelines have been hardened to securely sign
   binaries. There is now a separate signing stage so that signing
   keys are never exposed to build system code, and signing keys are
   ephemeral and only live as long as the signing pipeline stage.
   (#30753)

7. **Bootstrap mirror generation**

   The `spack bootstrap mirror` command can automatically create a
   mirror for bootstrapping the concretizer and other needed
   dependencies in an air-gapped environment. (#28556)

8. **Nascent Windows support**

   Spack now has initial support for Windows. Spack core has been
   refactored to run in the Windows environment, and a small number of
   packages can now build for Windows. More details are
   [in the documentation](https://spack.rtfd.io/en/latest/getting_started.html#spack-on-windows)
   (#27021, #28385, many more)

9. **Makefile generation**

   `spack env depfile` can be used to generate a `Makefile` from an
   environment, which can be used to build packages the environment
   in parallel on a single node. e.g.:

   ```console
   spack -e myenv env depfile > Makefile
   make
   ```

   Spack propagates `gmake` jobserver information to builds so that
   their jobs can share cores. (#30039, #30254, #30302, #30526)

10. **New variant features**

    In addition to being conditional themselves, variants can now have
    [conditional *values*](https://spack.readthedocs.io/en/latest/packaging_guide.html#conditional-possible-values)
    that are only possible for certain configurations of a package. (#29530)

    Variants can be
    [declared "sticky"](https://spack.readthedocs.io/en/latest/packaging_guide.html#sticky-variants),
    which prevents them from being enabled or disabled by the
    concretizer. Sticky variants must be set explicitly by users
    on the command line or in `packages.yaml`. (#28630)

* Allow conditional possible values in variants
* Add a "sticky" property to variants


## Other new features of note

* Environment views can optionally link only `run` dependencies
  with `link:run` (#29336)
* `spack external find --all` finds library-only packages in
  addition to build dependencies (#28005)
* Customizable `config:license_dir` option (#30135)
* `spack external find --path PATH` takes a custom search path (#30479)
* `spack spec` has a new `--format` argument like `spack find` (#27908)
* `spack concretize --quiet` skips printing concretized specs (#30272)
* `spack info` now has cleaner output and displays test info (#22097)
* Package-level submodule option for git commit versions (#30085, #30037)
* Using `/hash` syntax to refer to concrete specs in an environment
  now works even if `/hash` is not installed. (#30276)

## Major internal refactors

* full hash (see above)
* new develop versioning scheme `0.19.0-dev0`
* Allow for multiple dependencies/dependents from the same package (#28673)
* Splice differing virtual packages (#27919)

## Performance Improvements

* Concretization of large environments with `unify: when_possible` is
  much faster than concretizing separately (#28941, see above)
* Single-pass view generation algorithm is 2.6x faster (#29443)

## Archspec improvements

* `oneapi` and `dpcpp` flag support (#30783)
* better support for `M1` and `a64fx` (#30683)

## Removals and Deprecations

* Spack no longer supports Python `2.6` (#27256)
* Removed deprecated `--run-tests` option of `spack install`;
  use `spack test` (#30461)
* Removed deprecated `spack flake8`; use `spack style` (#27290)

* Deprecate `spack:concretization` config option; use
  `concretizer:unify` (#30038)
* Deprecate top-level module configuration; use module sets (#28659)
* `spack activate` and `spack deactivate` are deprecated in favor of
  environments; will be removed in `0.19.0` (#29430; see also `link:run`
  in #29336 above)

## Notable Bugfixes

* Fix bug that broke locks with many parallel builds (#27846)
* Many bugfixes and consistency improvements for the new concretizer
  and `--reuse` (#30357, #30092, #29835, #29933, #28605, #29694, #28848)

## Packages

* `CMakePackage` uses `CMAKE_INSTALL_RPATH_USE_LINK_PATH` (#29703)
* Refactored `lua` support: `lua-lang` virtual supports both
  `lua` and `luajit` via new `LuaPackage` build system(#28854)
* PythonPackage: now installs packages with `pip` (#27798)
* Python: improve site_packages_dir handling (#28346)
* Extends: support spec, not just package name (#27754)
* `find_libraries`: search for both .so and .dylib on macOS (#28924)
* Use stable URLs and `?full_index=1` for all github patches (#29239)

## Spack community stats

* 6,416 total packages, 458 new since `v0.17.0`
    * 219 new Python packages
    * 60 new R packages
* 377 people contributed to this release
    * 337 committers to packages
    * 85 committers to core

# v0.17.3 (2022-07-14)

### Spack bugfixes

* Fix missing chgrp on symlinks in package installations (#30743)
* Allow having non-existing upstreams (#30744, #30746)
* Fix `spack stage` with custom paths (#30448)
* Fix failing call for `spack buildcache save-specfile` (#30637)
* Fix globbing in compiler wrapper (#30699)

# v0.17.2 (2022-04-13)

### Spack bugfixes
* Fix --reuse with upstreams set in an environment (#29680)
* config add: fix parsing of validator error to infer type from oneOf (#29475)
* Fix spack -C command_line_scope used in conjunction with other flags (#28418)
* Use Spec.constrain to construct spec lists for stacks (#28783)
* Fix bug occurring when searching for inherited patches in packages (#29574)
* Fixed a few bugs when manipulating symlinks (#28318, #29515, #29636)
* Fixed a few minor bugs affecting command prompt, terminal title and argument completion (#28279, #28278, #28939, #29405, #29070, #29402)
* Fixed a few bugs affecting the spack ci command (#29518, #29419)
* Fix handling of Intel compiler environment (#29439)
* Fix a few edge cases when reindexing the DB (#28764)
* Remove "Known issues" from documentation (#29664)
* Other miscellaneous bugfixes (0b72e070583fc5bcd016f5adc8a84c99f2b7805f, #28403, #29261)

# v0.17.1 (2021-12-23)

### Spack Bugfixes
* Allow locks to work under high contention (#27846)
* Improve errors messages from clingo (#27707 #27970)
* Respect package permissions for sbang (#25764)
* Fix --enable-locks behavior (#24675)
* Fix log-format reporter ignoring install errors (#25961)
* Fix overloaded argparse keys (#27379)
* Allow style commands to run with targets other than "develop" (#27472)
* Log lock messages to debug level, instead of verbose level (#27408)
* Handle invalid unicode while logging (#21447)
* spack audit: fix API calls to variants (#27713)
* Provide meaningful message for empty environment installs (#28031)
* Added opensuse leap containers to spack containerize (#27837)
* Revert "patches: make re-applied patches idempotent" (#27625)
* MANPATH can use system defaults (#21682)
* Add "setdefault" subcommand to `spack module tcl` (#14686)
* Regenerate views when specs already installed (#28113)

### Package bugfixes
* Fix external package detection for OpenMPI (#27255)
* Update the UPC++ package to 2021.9.0 (#26996)
* Added py-vermin v1.3.2 (#28072)

# v0.17.0 (2021-11-05)

`v0.17.0` is a major feature release.

## Major features in this release

1. **New concretizer is now default**
   The new concretizer introduced as an experimental feature in `v0.16.0`
   is now the default (#25502). The new concretizer is based on the
   [clingo](https://github.com/potassco/clingo) logic programming system,
   and it enables us to do much higher quality and faster dependency solving
   The old concretizer is still available via the `concretizer: original`
   setting, but it is deprecated and will be removed in `v0.18.0`.

2. **Binary Bootstrapping**
   To make it easier to use the new concretizer and binary packages,
   Spack now bootstraps `clingo` and `GnuPG` from public binaries. If it
   is not able to bootstrap them from binaries, it installs them from
   source code. With these changes, you should still be able to clone Spack
   and start using it almost immediately. (#21446, #22354, #22489, #22606,
   #22720, #22720, #23677, #23946, #24003, #25138, #25607, #25964, #26029,
   #26399, #26599).

3. **Reuse existing packages (experimental)**
   The most wanted feature from our
   [2020 user survey](https://spack.io/spack-user-survey-2020/) and
   the most wanted Spack feature of all time (#25310). `spack install`,
   `spack spec`, and `spack concretize` now have a `--reuse` option, which
   causes Spack to minimize the number of rebuilds it does. The `--reuse`
   option will try to find existing installations and binary packages locally
   and in registered mirrors, and will prefer to use them over building new
   versions. This will allow users to build from source *far* less than in
   prior versions of Spack. This feature will continue to be improved, with
   configuration options and better CLI expected in `v0.17.1`. It will become
   the *default* concretization mode in `v0.18.0`.

4. **Better error messages**
   We have improved the error messages generated by the new concretizer by
   using *unsatisfiable cores*. Spack will now print a summary of the types
   of constraints that were violated to make a spec unsatisfiable (#26719).

5. **Conditional variants**
   Variants can now have a `when="<spec>"` clause, allowing them to be
   conditional based on the version or other attributes of a package (#24858).

6. **Git commit versions**
   In an environment and on the command-line, you can now provide a full,
   40-character git commit as a version for any package with a top-level
   `git` URL.  e.g., `spack install hdf5@45bb27f58240a8da7ebb4efc821a1a964d7712a8`.
   Spack will compare the commit to tags in the git repository to understand
   what versions it is ahead of or behind.

7. **Override local config and cache directories**
   You can now set `SPACK_DISABLE_LOCAL_CONFIG` to disable the `~/.spack` and
   `/etc/spack` configuration scopes. `SPACK_USER_CACHE_PATH` allows you to
   move caches out of `~/.spack`, as well (#27022, #26735). This addresses
   common problems where users could not isolate CI environments from local
   configuration.

8. **Improvements to Spack Containerize**
   For added reproducibility, you can now pin the Spack version used by
   `spack containerize` (#21910). The container build will only build
   with the Spack version pinned at build recipe creation instead of the
   latest Spack version.

9. **New commands for dealing with tags**
   The `spack tags` command allows you to list tags on packages (#26136), and you
   can list tests and filter tags with `spack test list` (#26842).

## Other new features of note

* Copy and relocate environment views as stand-alone installations (#24832)
* `spack diff` command can diff two installed specs (#22283, #25169)
* `spack -c <config>` can set one-off config parameters on CLI (#22251)
* `spack load --list` is an alias for `spack find --loaded` (#27184)
* `spack gpg` can export private key with `--secret` (#22557)
* `spack style` automatically bootstraps dependencies (#24819)
* `spack style --fix` automatically invokes `isort` (#24071)
* build dependencies can be installed from build caches with `--include-build-deps` (#19955)
* `spack audit` command for checking package constraints (#23053)
* Spack can now fetch from `CVS` repositories (yep, really) (#23212)
* `spack monitor` lets you upload analysis about installations to a
  [spack monitor server](https://github.com/spack/spack-monitor) (#23804, #24321,
  #23777, #25928))
* `spack python --path` shows which `python` Spack is using (#22006)
* `spack env activate --temp` can create temporary environments (#25388)
* `--preferred` and `--latest` options for `spack checksum` (#25830)
* `cc` is now pure posix and runs on Alpine (#26259)
* `SPACK_PYTHON` environment variable sets which `python` spack uses (#21222)
* `SPACK_SKIP_MODULES` lets you source `setup-env.sh` faster if you don't need modules (#24545)

## Major internal refactors

* `spec.yaml` files are now `spec.json`, yielding a large speed improvement (#22845)
* Splicing allows Spack specs to store mixed build provenance (#20262)
* More extensive hooks API for installations (#21930)
* New internal API for getting the active environment (#25439)

## Performance Improvements

* Parallelize separate concretization in environments; Previously 55 min E4S solve
    now takes 2.5 min (#26264)
* Drastically improve YamlFilesystemView file removal performance via batching (#24355)
* Speed up spec comparison (#21618)
* Speed up environment activation (#25633)

## Archspec improvements
* support for new generic `x86_64_v2`, `x86_64_v3`, `x86_64_v4` targets
    (see [archspec#31](https://github.com/archspec/archspec-json/pull/31))
* `spack arch --generic` lets you get the best generic architecture for
    your node (#27061)
* added support for aocc (#20124), `arm` compiler on `graviton2` (#24904)
    and on `a64fx` (#24524),

## Infrastructure, buildcaches, and services

* Add support for GCS Bucket Mirrors (#26382)
* Add `spackbot` to help package maintainers with notifications. See
  [spack.github.io/spackbot](https://spack.github.io/spackbot/)
* Reproducible pipeline builds with `spack ci rebuild` (#22887)
* Removed redundant concretizations from GitLab pipeline generation (#26622)
* Spack CI no longer generates jobs for unbuilt specs (#20435)
* Every pull request pipeline has its own buildcache (#25529)
* `--no-add` installs only specified specs and only if already present in… (#22657)
* Add environment-aware `spack buildcache sync` command (#25470)
* Binary cache installation speedups and improvements (#19690, #20768)

## Deprecations and Removals

* `spack setup` was deprecated in v0.16.0, and has now been removed.
  Use `spack develop` and `spack dev-build`.
* Remove unused `--dependencies` flag from `spack load` (#25731)
* Remove stubs for `spack module [refresh|find|rm|loads]`, all of which
  were deprecated in 2018.

## Notable Bugfixes

* Deactivate previous env before activating new one (#25409)
* Many fixes to error codes from `spack install` (#21319, #27012, #25314)
* config add: infer type based on JSON schema validation errors (#27035)
* `spack config edit` now works even if `spack.yaml` is broken (#24689)

## Packages

* Allow non-empty version ranges like `1.1.0:1.1` (#26402)
* Remove `.99`'s from many version ranges (#26422)
* Python: use platform-specific site packages dir (#25998)
* `CachedCMakePackage` for using *.cmake initial config files (#19316)
* `lua-lang` allows swapping `lua` and `luajit` (#22492)
* Better support for `ld.gold` and `ld.lld` (#25626)
* build times are now stored as metadata in `$prefix/.spack` (#21179)
* post-install tests can be reused in smoke tests (#20298)
* Packages can use `pypi` attribute to infer `homepage`/`url`/`list_url` (#17587)
* Use gnuconfig package for `config.guess` file replacement (#26035)
* patches: make re-applied patches idempotent (#26784)

## Spack community stats

* 5969 total packages, 920 new since `v0.16.0`
    * 358 new Python packages, 175 new R packages
* 513 people contributed to this release
    * 490 committers to packages
    * 105 committers to core
* Lots of GPU updates:
    * ~77 CUDA-related commits
    * ~66 AMD-related updates
    * ~27 OneAPI-related commits
    * 30 commits from AMD toolchain support
* `spack test` usage in packages is increasing
    * 1669 packages with tests (mostly generic python tests)
    * 93 packages with their own tests


# v0.16.3 (2021-09-21)

* clang/llvm: fix version detection (#19978)
* Fix use of quotes in Python build system (#22279)
* Cray: fix extracting paths from module files (#23472)
* Use AWS CloudFront for source mirror (#23978)
* Ensure all roots of an installed environment are marked explicit in db (#24277)
* Fix fetching for Python 3.8 and 3.9 (#24686)
* locks: only open lockfiles once instead of for every lock held (#24794)
* Remove the EOL centos:6 docker image

# v0.16.2 (2021-05-22)

* Major performance improvement for `spack load` and other commands. (#23661)
* `spack fetch` is now environment-aware. (#19166)
* Numerous fixes for the new, `clingo`-based concretizer. (#23016, #23307,
  #23090, #22896, #22534, #20644, #20537, #21148)
* Supoprt for automatically bootstrapping `clingo` from source. (#20652, #20657
  #21364, #21446, #21913, #22354, #22444, #22460, #22489, #22610, #22631)
* Python 3.10 support: `collections.abc` (#20441)
* Fix import issues by using `__import__` instead of Spack package importe.
  (#23288, #23290)
* Bugfixes and `--source-dir` argument for `spack location`. (#22755, #22348,
  #22321)
* Better support for externals in shared prefixes. (#22653)
* `spack build-env` now prefers specs defined in the active environment.
  (#21642)
* Remove erroneous warnings about quotes in `from_sourcing_files`. (#22767)
* Fix clearing cache of `InternalConfigScope`. (#22609)
* Bugfix for active when pkg is already active error. (#22587)
* Make `SingleFileScope` able to repopulate the cache after clearing it.
  (#22559)
* Channelflow: Fix the package. (#22483)
* More descriptive error message for bugs in `package.py` (#21811)
* Use package-supplied `autogen.sh`. (#20319)
* Respect `-k/verify-ssl-false` in `_existing_url` method. (#21864)


# v0.16.1 (2021-02-22)

This minor release includes a new feature and associated fixes:
* intel-oneapi support through new packages (#20411, #20686, #20693, #20717,
  #20732, #20808, #21377, #21448)

This release also contains bug fixes/enhancements for:
* HIP/ROCm support (#19715, #20095)
* concretization (#19988, #20020, #20082, #20086, #20099, #20102, #20128,
  #20182, #20193, #20194, #20196, #20203, #20247, #20259, #20307, #20362,
  #20383, #20423, #20473, #20506, #20507, #20604, #20638, #20649, #20677,
  #20680, #20790)
* environment install reporting fix (#20004)
* avoid import in ABI compatibility info (#20236)
* restore ability of dev-build to skip patches (#20351)
* spack find -d spec grouping (#20028)
* spack smoke test support (#19987, #20298)
* macOS fixes (#20038, #21662)
* abstract spec comparisons (#20341)
* continuous integration (#17563)
* performance improvements for binary relocation (#19690, #20768)
* additional sanity checks for variants in builtin packages (#20373)
* do not pollute auto-generated configuration files with empty lists or
  dicts (#20526)

plus assorted documentation (#20021, #20174) and package bug fixes/enhancements
(#19617, #19933, #19986, #20006, #20097, #20198, #20794, #20906, #21411).


# v0.16.0 (2020-11-18)

`v0.16.0` is a major feature release.

## Major features in this release

1. **New concretizer (experimental)** Our new backtracking concretizer is
   now in Spack as an experimental feature. You will need to install
   `clingo@master+python` and set `concretizer: clingo` in `config.yaml`
   to use it. The original concretizer is not exhaustive and is not
   guaranteed to find a solution if one exists. We encourage you to use
   the new concretizer and to report any bugs you find with it. We
   anticipate making the new concretizer the default and including all
   required dependencies for it in Spack `v0.17`. For more details, see
   #19501.

2. **spack test (experimental)** Users can add `test()` methods to their
   packages to run smoke tests on installations with the new `spack test`
   command (the old `spack test` is now `spack unit-test`). `spack test`
   is environment-aware, so you can `spack install` an environment and
   `spack test run` smoke tests on all of its packages. Historical test
   logs can be perused with `spack test results`. Generic smoke tests for
   MPI implementations, C, C++, and Fortran compilers as well as specific
   smoke tests for 18 packages. This is marked experimental because the
   test API (`self.run_test()`) is likely to be change, but we encourage
   users to upstream tests, and we will maintain and refactor any that
   are added to mainline packages (#15702).

3. **spack develop** New `spack develop` command allows you to develop
   several packages at once within a Spack environment. Running
   `spack develop foo@v1` and `spack develop bar@v2` will check
    out specific versions of `foo` and `bar` into subdirectories, which you
    can then build incrementally with `spack install ` (#15256).

4. **More parallelism** Spack previously installed the dependencies of a
   _single_ spec in parallel. Entire environments can now be installed in
   parallel, greatly accelerating builds of large environments. get
   parallelism from individual specs. Spack now parallelizes entire
   environment builds (#18131).

5. **Customizable base images for spack containerize**
    `spack containerize` previously only output a `Dockerfile` based
    on `ubuntu`. You may now specify any base image of your choosing (#15028).

6. **more external finding** `spack external find` was added in `v0.15`,
   but only `cmake` had support. `spack external find` can now find
   `bison`, `cuda`, `findutils`, `flex`, `git`, `lustre` `m4`, `mpich`,
   `mvapich2`, `ncurses`, `openmpi`, `perl`, `spectrum-mpi`, `tar`, and
   `texinfo` on your system and add them automatically to
   `packages.yaml`.

7. **Support aocc, nvhpc, and oneapi compilers** We are aggressively
   pursuing support for the newest vendor compilers, especially those for
   the U.S. exascale and pre-exascale systems. Compiler classes and
   auto-detection for `aocc`, `nvhpc`, `oneapi` are now in Spack (#19345,
   #19294, #19330).

## Additional new features of note

* New `spack mark` command can be used to designate packages as explicitly
  installed, so that `spack gc` will not garbage-collect them (#16662).
* `install_tree` can be customized with Spack's projection format (#18341)
* `sbang` now lives in the `install_tree` so that all users can access it (#11598)
* `csh` and `tcsh` users no longer need to set `SPACK_ROOT` before
  sourcing `setup-env.csh` (#18225)
* Spec syntax now supports `variant=*` syntax for finding any package
  that has a particular variant (#19381).
* Spack respects `SPACK_GNUPGHOME` variable for custom GPG directories (#17139)
* Spack now recognizes Graviton chips

## Major refactors

* Use spawn instead of fork on Python >= 3.8 on macOS (#18205)
* Use indexes for public build caches (#19101, #19117, #19132, #19141,  #19209)
* `sbang` is an external package now (https://github.com/spack/sbang, #19582)
* `archspec` is an external package now (https://github.com/archspec/archspec, #19600)

## Deprecations and Removals

* `spack bootstrap` was deprecated in v0.14.0, and has now been removed.
* `spack setup` is deprecated as of v0.16.0.
* What was `spack test` is now called `spack unit-test`. `spack test` is
  now the smoke testing feature in (2) above.

## Bugfixes

Some of the most notable bugfixes in this release include:

* Better warning messages for deprecated syntax in `packages.yaml` (#18013)
* `buildcache list --allarch` now works properly (#17827)
* Many fixes and tests for buildcaches and binary relcoation (#15687,
  *#17455, #17418, #17455, #15687, #18110)

## Package Improvements

Spack now has 5050 total packages, 720 of which were added since `v0.15`.

* ROCm packages (`hip`, `aomp`, more) added by AMD (#19957, #19832, others)
* Many improvements for ARM support
* `llvm-flang`, `flang`, and `f18` removed, as `llvm` has real `flang`
  support since Flang was merged to LLVM mainline
* Emerging support for `spack external find` and `spack test` in packages.

## Infrastructure

* Major infrastructure improvements to pipelines on `gitlab.spack.io`
* Support for testing PRs from forks (#19248) is being enabled for all
  forks to enable rolling, up-to-date binary builds on `develop`


# v0.15.4 (2020-08-12)

This release contains one feature addition:

* Users can set `SPACK_GNUPGHOME` to override Spack's GPG path (#17139)

Several bugfixes for CUDA, binary packaging, and `spack -V`:

* CUDA package's `.libs` method searches for `libcudart` instead of `libcuda` (#18000)
* Don't set `CUDAHOSTCXX` in environments that contain CUDA (#17826)
* `buildcache create`: `NoOverwriteException` is a warning, not an error (#17832)
* Fix `spack buildcache list --allarch` (#17884)
* `spack -V` works with `releases/latest` tag and shallow clones (#17884)

And fixes for GitHub Actions and tests to ensure that CI passes on the
release branch (#15687, #17279, #17328, #17377, #17732).

# v0.15.3 (2020-07-28)

This release contains the following bugfixes:

* Fix handling of relative view paths (#17721)
* Fixes for binary relocation (#17418, #17455)
* Fix redundant printing of error messages in build environment (#17709)

It also adds a support script for Spack tutorials:

* Add a tutorial setup script to share/spack (#17705, #17722)

# v0.15.2 (2020-07-23)

This minor release includes two new features:

* Spack install verbosity is decreased, and more debug levels are added (#17546)
* The $spack/share/spack/keys directory contains public keys that may be optionally trusted for public binary mirrors (#17684)

This release also includes several important fixes:

* MPICC and related variables are now cleand in the build environment (#17450)
* LLVM flang only builds CUDA offload components when +cuda (#17466)
* CI pipelines no longer upload user environments that can contain secrets to the internet (#17545)
* CI pipelines add bootstrapped compilers to the compiler config (#17536)
* `spack buildcache list` does not exit on first failure and lists later mirrors (#17565)
* Apple's "gcc" executable that is an apple-clang compiler does not generate a gcc compiler config (#17589)
* Mixed compiler toolchains are merged more naturally across different compiler suffixes (#17590)
* Cray Shasta platforms detect the OS properly (#17467)
* Additional more minor fixes.

# v0.15.1 (2020-07-10)

This minor release includes several important fixes:

* Fix shell support on Cray (#17386)
* Fix use of externals installed with other Spack instances (#16954)
* Fix gcc+binutils build (#9024)
* Fixes for usage of intel-mpi (#17378 and #17382)
* Fixes to Autotools config.guess detection (#17333 and #17356)
* Update `spack install` message to prompt user when an environment is not
  explicitly activated (#17454)

This release also adds a mirror for all sources that are
fetched in Spack (#17077). It is expected to be useful when the
official website for a Spack package is unavailable.

# v0.15.0 (2020-06-28)

`v0.15.0` is a major feature release.

## Major Features in this release

1. **Cray support** Spack will now work properly on Cray "Cluster"
systems (non XC systems) and after a `module purge` command on Cray
systems. See #12989

2. **Virtual package configuration** Virtual packages are allowed in
packages.yaml configuration. This allows users to specify a virtual
package as non-buildable without needing to specify for each
implementation. See #14934

3. **New config subcommands** This release adds `spack config add` and
`spack config remove` commands to add to and remove from yaml
configuration files from the CLI. See #13920

4. **Environment activation** Anonymous environments are **no longer**
automatically activated in the current working directory. To activate
an environment from a `spack.yaml` file in the current directory, use
the `spack env activate .` command. This removes a concern that users
were too easily polluting their anonymous environments with accidental
installations. See #17258

5. **Apple clang compiler** The clang compiler and the apple-clang
compiler are now separate compilers in Spack. This allows Spack to
improve support for the apple-clang compiler. See #17110

6. **Finding external packages** Spack packages can now support an API
for finding external installations. This allows the `spack external
find` command to automatically add installations of those packages to
the user's configuration. See #15158


## Additional new features of note

* support for using Spack with the fish shell (#9279)
* `spack load --first` option to load first match (instead of prompting user) (#15622)
* support the Cray cce compiler both new and classic versions (#17256, #12989)
* `spack dev-build` command:
  * supports stopping before a specified phase (#14699)
  * supports automatically launching a shell in the build environment (#14887)
* `spack install --fail-fast` allows builds to fail at the first error (rather than best-effort) (#15295)
* environments: SpecList references can be dereferenced as compiler or dependency constraints (#15245)
* `spack view` command: new support for a copy/relocate view type (#16480)
* ci pipelines: see documentation for several improvements
* `spack mirror -a` command now supports excluding packages (#14154)
* `spack buildcache create` is now environment-aware (#16580)
* module generation: more flexible format for specifying naming schemes (#16629)
* lmod module generation: packages can be configured as core specs for lmod hierarchy (#16517)

## Deprecations and Removals

The following commands were deprecated in v0.13.0, and have now been removed:

* `spack configure`
* `spack build`
* `spack diy`

The following commands were deprecated in v0.14.0, and will be removed in the next major release:

* `spack bootstrap`

## Bugfixes

Some of the most notable bugfixes in this release include:

* Spack environments can now contain the string `-h` (#15429)
* The `spack install` gracefully handles being backgrounded (#15723, #14682)
* Spack uses `-isystem` instead of `-I` in cases that the underlying build system does as well (#16077)
* Spack no longer prints any specs that cannot be safely copied into a Spack command (#16462)
* Incomplete Spack environments containing python no longer cause problems (#16473)
* Several improvements to binary package relocation

## Package Improvements

The Spack project is constantly engaged in routine maintenance,
bugfixes, and improvements for the package ecosystem. Of particular
note in this release are the following:

* Spack now contains 4339 packages. There are 430 newly supported packages in v0.15.0
* GCC now builds properly on ARM architectures (#17280)
* Python: patched to support compiling mixed C/C++ python modules through distutils (#16856)
* improvements to pytorch and py-tensorflow packages
* improvements to major MPI implementations: mvapich2, mpich, openmpi, and others

## Spack Project Management:

* Much of the Spack CI infrastructure has moved from Travis to GitHub Actions (#16610, #14220, #16345)
* All merges to the `develop` branch run E4S CI pipeline (#16338)
* New `spack debug report` command makes reporting bugs easier (#15834)

# v0.14.2 (2020-04-15)

This is a minor release on the `0.14` series. It includes performance
improvements and bug fixes:

* Improvements to how `spack install` handles foreground/background (#15723)
* Major performance improvements for reading the package DB (#14693, #15777)
* No longer check for the old `index.yaml` database file (#15298)
* Properly activate environments with '-h' in the name (#15429)
* External packages have correct `.prefix` in environments/views (#15475)
* Improvements to computing env modifications from sourcing files (#15791)
* Bugfix on Cray machines when getting `TERM` env variable (#15630)
* Avoid adding spurious `LMOD` env vars to Intel modules (#15778)
* Don't output [+] for mock installs run during tests (#15609)

# v0.14.1 (2020-03-20)

This is a bugfix release on top of `v0.14.0`.  Specific fixes include:

* several bugfixes for parallel installation (#15339, #15341, #15220, #15197)
* `spack load` now works with packages that have been renamed (#14348)
* bugfix for `suite-sparse` installation (#15326)
* deduplicate identical suffixes added to module names (#14920)
* fix issues with `configure_args` during module refresh (#11084)
* increased test coverage and test fixes (#15237, #15354, #15346)
* remove some unused code (#15431)

# v0.14.0 (2020-02-23)

`v0.14.0` is a major feature release, with 3 highlighted features:

1. **Distributed builds.** Multiple Spack instances will now coordinate
   properly with each other through locks. This works on a single node
   (where you've called `spack` several times) or across multiple nodes
   with a shared filesystem. For example, with SLURM, you could build
   `trilinos` and its dependencies on 2 24-core nodes, with 3 Spack
   instances per node and 8 build jobs per instance, with `srun -N 2 -n 6
   spack install -j 8 trilinos`. This requires a filesystem with locking
   enabled, but not MPI or any other library for parallelism.

2.  **Build pipelines.** You can also build in parallel through Gitlab
   CI. Simply create a Spack environment and push it to Gitlab to build
   on Gitlab runners. Pipeline support is now integrated into a single
   `spack ci` command, so setting it up is easier than ever.  See the
   [Pipelines section](https://spack.readthedocs.io/en/v0.14.0/pipelines.html)
   in the docs.

3. **Container builds.** The new `spack containerize` command allows you
   to create a Docker or Singularity recipe from any Spack environment.
   There are options to customize the build if you need them. See the
   [Container Images section](https://spack.readthedocs.io/en/latest/containers.html)
   in the docs.

In addition, there are several other new commands, many bugfixes and
improvements, and `spack load` no longer requires modules, so you can use
it the same way on your laptop or on your supercomputer.

Spack grew by over 300 packages since our last release in November 2019,
and the project grew to over 500 contributors.  Thanks to all of you for
making yet another great release possible. Detailed notes below.

## Major new core features
* Distributed builds: spack instances coordinate and build in parallel (#13100)
* New `spack ci` command to manage CI pipelines (#12854)
* Generate container recipes from environments: `spack containerize` (#14202)
* `spack load` now works without using modules (#14062, #14628)
* Garbage collect old/unused installations with `spack gc` (#13534)
* Configuration files all set environment modifications the same way (#14372,
  [docs](https://spack.readthedocs.io/en/v0.14.0/configuration.html#environment-modifications))
* `spack commands --format=bash` auto-generates completion (#14393, #14607)
* Packages can specify alternate fetch URLs in case one fails (#13881)

## Improvements
* Improved locking for concurrency with environments (#14676, #14621, #14692)
* `spack test` sends args to `pytest`, supports better listing (#14319)
* Better support for aarch64 and cascadelake microarch (#13825, #13780, #13820)
* Archspec is now a separate library (see https://github.com/archspec/archspec)
* Many improvements to the `spack buildcache` command (#14237, #14346,
  #14466, #14467, #14639, #14642, #14659, #14696, #14698, #14714, #14732,
  #14929, #15003, #15086, #15134)

## Selected Bugfixes
* Compilers now require an exact match on version (#8735, #14730, #14752)
* Bugfix for patches that specified specific versions (#13989)
* `spack find -p` now works in environments (#10019, #13972)
* Dependency queries work correctly in `spack find` (#14757)
* Bugfixes for locking upstream Spack instances chains (#13364)
* Fixes for PowerPC clang optimization flags (#14196)
* Fix for issue with compilers and specific microarchitectures (#13733, #14798)

## New commands and options
* `spack ci` (#12854)
* `spack containerize` (#14202)
* `spack gc` (#13534)
* `spack load` accepts `--only package`, `--only dependencies` (#14062, #14628)
* `spack commands --format=bash` (#14393)
* `spack commands --update-completion` (#14607)
* `spack install --with-cache` has new option: `--no-check-signature` (#11107)
* `spack test` now has `--list`, `--list-long`, and `--list-names` (#14319)
* `spack install --help-cdash` moves CDash help out of the main help (#13704)

## Deprecations
* `spack release-jobs` has been rolled into `spack ci`
* `spack bootstrap` will be removed in a future version, as it is no longer
  needed to set up modules (see `spack load` improvements above)

## Documentation
* New section on building container images with Spack (see
  [docs](https://spack.readthedocs.io/en/latest/containers.html))
* New section on using `spack ci` command to build pipelines (see
  [docs](https://spack.readthedocs.io/en/latest/pipelines.html))
* Document how to add conditional dependencies (#14694)
* Document how to use Spack to replace Homebrew/Conda (#13083, see
  [docs](https://spack.readthedocs.io/en/latest/workflows.html#using-spack-to-replace-homebrew-conda))

## Important package changes
* 3,908 total packages (345 added since 0.13.0)
* Added first cut at a TensorFlow package (#13112)
* We now build R without "recommended" packages, manage them w/Spack (#12015)
* Elpa and OpenBLAS now leverage microarchitecture support (#13655, #14380)
* Fix `octave` compiler wrapper usage (#14726)
* Enforce that packages in `builtin` aren't missing dependencies (#13949)


# v0.13.4 (2020-02-07)

This release contains several bugfixes:

* bugfixes for invoking python in various environments (#14349, #14496, #14569)
* brought tab completion up to date (#14392)
* bugfix for removing extensions from views in order (#12961)
* bugfix for nondeterministic hashing for specs with externals (#14390)

# v0.13.3 (2019-12-23)

This release contains more major performance improvements for Spack
environments, as well as bugfixes for mirrors and a `python` issue with
RHEL8.

* mirror bugfixes: symlinks, duplicate patches, and exception handling (#13789)
* don't try to fetch `BundlePackages` (#13908)
* avoid re-fetching patches already added to a mirror (#13908)
* avoid re-fetching already added patches (#13908)
* avoid re-fetching already added patches (#13908)
* allow repeated invocations of `spack mirror create` on the same dir (#13908)
* bugfix for RHEL8 when `python` is unavailable (#14252)
* improve concretization performance in environments (#14190)
* improve installation performance in environments (#14263)

# v0.13.2 (2019-12-04)

This release contains major performance improvements for Spack environments, as
well as some bugfixes and minor changes.

* allow missing modules if they are blacklisted (#13540)
* speed up environment activation (#13557)
* mirror path works for unknown versions (#13626)
* environments: don't try to modify run-env if a spec is not installed (#13589)
* use semicolons instead of newlines in module/python command (#13904)
* verify.py: os.path.exists exception handling (#13656)
* Document use of the maintainers field (#13479)
* bugfix with config caching (#13755)
* hwloc: added 'master' version pointing at the HEAD of the master branch (#13734)
* config option to allow gpg warning suppression (#13744)
* fix for relative symlinks when relocating binary packages (#13727)
* allow binary relocation of strings in relative binaries (#13724)

# v0.13.1 (2019-11-05)

This is a bugfix release on top of `v0.13.0`.  Specific fixes include:

* `spack find` now displays variants and other spec constraints
* bugfix: uninstall should find concrete specs by DAG hash (#13598)
* environments: make shell modifications partially unconditional (#13523)
* binary distribution: relocate text files properly in relative binaries (#13578)
* bugfix: fetch prefers to fetch local mirrors over remote resources (#13545)
* environments: only write when necessary (#13546)
* bugfix: spack.util.url.join() now handles absolute paths correctly (#13488)
* sbang: use utf-8 for encoding when patching (#13490)
* Specs with quoted flags containing spaces are parsed correctly (#13521)
* targets: print a warning message before downgrading (#13513)
* Travis CI: Test Python 3.8 (#13347)
* Documentation: Database.query methods share docstrings (#13515)
* cuda: fix conflict statements for x86-64 targets (#13472)
* cpu: fix clang flags for generic x86_64 (#13491)
* syaml_int type should use int.__repr__ rather than str.__repr__ (#13487)
* elpa: prefer 2016.05.004 until sse/avx/avx2 issues are resolved (#13530)
* trilinos: temporarily constrain netcdf@:4.7.1 (#13526)

# v0.13.0 (2019-10-25)

`v0.13.0` is our biggest Spack release yet, with *many* new major features.
From facility deployment to improved environments, microarchitecture
support, and auto-generated build farms, this release has features for all of
our users.

Spack grew by over 700 packages in the past year, and the project now has
over 450 contributors.  Thanks to all of you for making this release possible.

## Major new core features
- Chaining: use dependencies from external "upstream" Spack instances
- Environments now behave more like virtualenv/conda
  - Each env has a *view*: a directory with all packages symlinked in
  - Activating an environment sets `PATH`, `LD_LIBRARY_PATH`, `CPATH`,
    `CMAKE_PREFIX_PATH`, `PKG_CONFIG_PATH`, etc. to point to this view.
- Spack detects and builds specifically for your microarchitecture
  - named, understandable targets like `skylake`, `broadwell`, `power9`, `zen2`
  - Spack knows which compilers can build for which architectures
  - Packages can easily query support for features like `avx512` and `sse3`
  - You can pick a target with, e.g. `spack install foo target=icelake`
- Spack stacks: combinatorial environments for facility deployment
  - Environments can now build cartesian products of specs (with `matrix:`)
  - Conditional syntax support to exclude certain builds from the stack
- Projections: ability to build easily navigable symlink trees environments
- Support no-source packages (BundlePackage) to aggregate related packages
- Extensions: users can write custom commands that live outside of Spack repo
- Support ARM and Fujitsu compilers

## CI/build farm support
- `spack release-jobs` can detect `package.py` changes and generate
    `.gitlab-ci.yml` to create binaries for an environment or stack
	in parallel (initial support -- will change in future release).
- Results of build pipelines can be uploaded to a CDash server.
- Spack can now upload/fetch from package mirrors in Amazon S3

## New commands/options
- `spack mirror create --all` downloads *all* package sources/resources/patches
- `spack dev-build` runs phases of the install pipeline on the working directory
- `spack deprecate` permanently symlinks an old, unwanted package to a new one
- `spack verify` chcecks that packages' files match what was originally installed
- `spack find --json` prints `JSON` that is easy to parse with, e.g. `jq`
- `spack find --format FORMAT` allows you to flexibly print package metadata
- `spack spec --json` prints JSON version of `spec.yaml`

## Selected improvements
- Auto-build requested compilers if they do not exist
- Spack automatically adds `RPATHs` needed to make executables find compiler
    runtime libraries (e.g., path to newer `libstdc++` in `icpc` or `g++`)
- setup-env.sh is now compatible with Bash, Dash, and Zsh
- Spack now caps build jobs at min(16, ncores) by default
- `spack compiler find` now also throttles number of spawned processes
- Spack now writes stage directories directly to `$TMPDIR` instead of
    symlinking stages within `$spack/var/spack/cache`.
- Improved and more powerful `spec` format strings
- You can pass a `spec.yaml` file anywhere in the CLI you can type a spec.
- Many improvements to binary caching
- Gradually supporting new features from Environment Modules v4
- `spack edit` respects `VISUAL` environment variable
- Simplified package syntax for specifying build/run environment modifications
- Numerous improvements to support for environments across Spack commands
- Concretization improvements

## Documentation
- Multi-lingual documentation (Started a Japanese translation)
- Tutorial now has its own site at spack-tutorial.readthedocs.io
  - This enables us to keep multiple versions of the tutorial around

## Deprecations
- Spack no longer supports dotkit (LLNL's homegrown, now deprecated module tool)
- `spack build`, `spack configure`, `spack diy` deprecated in favor of
    `spack dev-build` and `spack install`

## Important package changes
- 3,563 total packages (718 added since 0.12.1)
- Spack now defaults to Python 3 (previously preferred 2.7 by default)
- Much improved ARM support thanks to Fugaku (RIKEN) and SNL teams
- Support new special versions: master, trunk, and head (in addition to develop)
- Better finding logic for libraries and headers


# v0.12.1 (2018-11-13)

This is a minor bugfix release, with a minor fix in the tutorial and a `flake8` fix.

Bugfixes
* Add `r` back to regex strings in binary distribution
* Fix gcc install version in the tutorial


# v0.12.0 (2018-11-13)

## Major new features
- Spack environments
- `spack.yaml` and `spack.lock` files for tracking dependencies
- Custom configurations via command line
- Better support for linking Python packages into view directories
- Packages have more control over compiler flags via flag handlers
- Better support for module file generation
- Better support for Intel compilers, Intel MPI, etc.
- Many performance improvements, improved startup time

## License
- As of this release, all of Spack is permissively licensed under Apache-2.0 or MIT, at the user's option.
- Consents from over 300 contributors were obtained to make this relicense possible.
- Previous versions were distributed under the LGPL license, version 2.1.

## New packages
Over 2,900 packages (800 added since last year)

Spack would not be possible without our community.  Thanks to all of our
[contributors](https://github.com/spack/spack/graphs/contributors) for the
new features and packages in this release!


# v0.11.2 (2018-02-07)

This release contains the following fixes:

* Fixes for `gfortran` 7 compiler detection (#7017)
* Fixes for exceptions thrown during module generation (#7173)


# v0.11.1 (2018-01-19)

This release contains bugfixes for compiler flag handling.  There were issues in `v0.11.0` that caused some packages to be built without proper optimization.

Fixes:
* Issue #6999: FFTW installed with Spack 0.11.0 gets built without optimisations

Includes:
* PR #6415: Fixes for flag handling behavior
* PR #6960: Fix type issues with setting flag handlers
* 880e319: Upstream fixes to `list_url` in various R packages


# v0.11.0 (2018-01-17)

Spack v0.11.0 contains many improvements since v0.10.0.
Below is a summary of the major features, broken down by category.

## New packages
- Spack now has 2,178 packages (from 1,114 in v0.10.0)
- Many more Python packages (356) and R packages (471)
- 48 Exascale Proxy Apps (try `spack list -t proxy-app`)


## Core features for users
- Relocatable binary packages (`spack buildcache`, #4854)
- Spack now fully supports Python 3 (#3395)
- Packages can be tagged and searched by tags (#4786)
- Custom module file templates using Jinja (#3183)
- `spack bootstrap` command now sets up a basic module environment (#3057)
- Simplified and better organized help output (#3033)
- Improved, less redundant `spack install` output (#5714, #5950)
- Reworked `spack dependents` and `spack dependencies` commands (#4478)


## Major new features for packagers
- Multi-valued variants (#2386)
- New `conflicts()` directive (#3125)
- New dependency type: `test` dependencies (#5132)
- Packages can require their own patches on dependencies (#5476)
  - `depends_on(..., patches=<patch list>)`
- Build interface for passing linker information through Specs (#1875)
  - Major packages that use blas/lapack now use this interface
- Flag handlers allow packages more control over compiler flags (#6415)
- Package subclasses support many more build systems:
  - autotools, perl, qmake, scons, cmake, makefile, python, R, WAF
  - package-level support for installing Intel HPC products (#4300)
- `spack blame` command shows contributors to packages (#5522)
- `spack create` now guesses many more build systems (#2707)
- Better URL parsing to guess package version URLs (#2972)
- Much improved `PythonPackage` support (#3367)


## Core
- Much faster concretization (#5716, #5783)
- Improved output redirection (redirecting build output works properly #5084)
- Numerous improvements to internal structure and APIs


## Tutorials & Documentation
- Many updates to documentation
- [New tutorial material from SC17](https://spack.readthedocs.io/en/latest/tutorial.html)
  - configuration
  - build systems
  - build interface
  - working with module generation
- Documentation on docker workflows and best practices


## Selected improvements and bug fixes
- No longer build Python eggs -- installations are plain directories (#3587)
- Improved filtering of system paths from build PATHs and RPATHs (#2083, #3910)
- Git submodules are properly handled on fetch (#3956)
- Can now set default number of parallel build jobs in `config.yaml`
- Improvements to `setup-env.csh` (#4044)
- Better default compiler discovery on Mac OS X (#3427)
  - clang will automatically mix with gfortran
- Improved compiler detection on Cray machines (#3075)
- Better support for IBM XL compilers
- Better tab completion
- Resume gracefully after prematurely terminated partial installs (#4331)
- Better mesa support (#5170)


Spack would not be possible without our community.  Thanks to all of our
[contributors](https://github.com/spack/spack/graphs/contributors) for the
new features and packages in this release!


# v0.10.0 (2017-01-17)

This is Spack `v0.10.0`.  With this release, we will start to push Spack
releases more regularly.  This is the last Spack release without
automated package testing.  With the next release, we will begin to run
package tests in addition to unit tests.

Spack has grown rapidly from 422 to
[1,114 packages](https://spack.readthedocs.io/en/v0.10.0/package_list.html),
thanks to the hard work of over 100 contributors.  Below is a condensed
version of all the changes since `v0.9.1`.

### Packages
- Grew from 422 to 1,114 packages
  - Includes major updates like X11, Qt
  - Expanded HPC, R, and Python ecosystems

### Core
- Major speed improvements for spack find and concretization
- Completely reworked architecture support
  - Platforms can have front-end and back-end OS/target combinations
  - Much better support for Cray and BG/Q cross-compiled environments
- Downloads are now cached locally
- Support installations in deeply nested directories: patch long shebangs using `sbang`

### Basic usage
- Easier global configuration via config.yaml
  - customize install, stage, and cache locations
- Hierarchical configuration scopes: default, site, user
  - Platform-specific scopes allow better per-platform defaults
- Ability to set `cflags`, `cxxflags`, `fflags` on the command line
- YAML-configurable support for both Lmod and tcl modules in mainline
- `spack install` supports --dirty option for emergencies

### For developers
- Support multiple dependency types: `build`, `link`, and `run`
- Added `Package` base classes for custom build systems
  - `AutotoolsPackage`, `CMakePackage`, `PythonPackage`, etc.
  - `spack create` now guesses many more build systems
- Development environment integration with `spack setup`
- New interface to pass linking information via `spec` objects
  - Currently used for `BLAS`/`LAPACK`/`SCALAPACK` libraries
  - Polymorphic virtual dependency attributes: `spec['blas'].blas_libs`

### Testing & Documentation
- Unit tests run continuously on Travis CI for Mac and Linux
- Switched from `nose` to `pytest` for unit tests.
  - Unit tests take 1 minute now instead of 8
- Massively expanded documentation
- Docs are now hosted on [spack.readthedocs.io](https://spack.readthedocs.io)
