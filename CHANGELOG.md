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
* avoid re-fetching alread added patches (#13908)
* avoid re-fetching alread added patches (#13908)
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
- Docs are now hosted on [spack.readthedocs.io](http://spack.readthedocs.io)
