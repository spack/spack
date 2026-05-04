# Spack Smoke/Integration Testing

Tests production context runs of Spack

* Isolates behavior from individual package quirks
* Guarantees builds without worrying about Gitlab CI's pruning mechanisms (no "nothing to rebuild")
* Directly tests specific Spack behaviors via controlled, deliberatly composed packages and generated source code relying on those behaviors
* Production style useage of Spack allows a deliberate testing environment beyond the limited and contrived nature of unit tests
* In the event of failure revealed by the integration tests, allows for much faster development cycles without needing to wait
hours for Gitlab to complete.
* Reduces AWS costs by catching some failures before kicking off expensive Gitlab CI pipelines

## Currently Tested Behavior

Compiler and Package detection

* Adding a repo beyond builtin and utilizing packages from it

* Fetching a package's source from a local file url

* Successfully staging a packages source

* Executing a build system and driving the build of that system

* Installing the package from the build tree

* Tests ability to run package defined tests
  * Run them to verify a correct installation

Each of these higher level tasks exercises many more atomic sections of Spack that are well covered by our unit tests.
The purpose served by these tests is to validate the integration and compatibility of each of these more atomic components

## Adding More Integration Tests

Current approach for adding a new integration test:

* Define a new package in `var/spack/test_repos/spack_repo/integration_test/x`
* Define the source code for `x` in `var/spack/test_repos/spack_repo/integration_test/x/x-src` (place makefile, configure script, etc. here)
* A single version declaration like `version("0.1")` (no hash) is recommended
* Add `x` as a root spec to `var/spack/test_repos/spack_repo/integration_test/integration_env/spack.yaml`

That's all you should need to do. Other notes about the process:

* The script `develop_env_specs.py` uses `spack develop` on `x` with `x-src`
  * This setup makes it easy to change source files inside `x-src` without updating any hashes
  * At the moment it would be awkward to maintain multiple versions of the source (although `develop_env_specs` could be updated to use different source directories depending on the version of the package)
  * Generally speaking the focus on this repo is not on modeling variants/versions (concretization unit tests already do a good job of that)
* Note that packages in `integration_test` repo make use of packages in the builtin repo, e.g. using the builtin CMake build-system definition. For build systems `spack external add` is used in the CI script (but if you add a package that depends on a new build system, you'll have to check the CI script for this).

### Roadmap for future Tests

#### Build systems

Planned coverage:

* ~~CMake~~
* Autotools
* Meson
* Make/NMake
* MsBuild
* Go
* Cargo
* Python

#### Platforms

Target behavior on specific

* Platforms
* Architectures
* Operating Systems

#### Fetch types

* Https
* Ssh
* Git
* Bundle (no fetch)
* etc

#### Mirrors

Test setting up and pulling from a mirror

#### Configurations

Different Configurations of Spack

* Concretizer settings
* Config settings
* Includes (Optional path, git, etc)
* Environment settings
* Mirror settings
* Package settings
* View settings

#### Repositories

 More complex repo setups

* Multi-package repository repos
* Mixed package API versions
* etc

#### Packages

Packages doing more complex things

* Packages with more complex configuration
* Packages with dependencies
* Virtual packages
* Bundle Packages

#### Libraries and Executables

Test building, linking, running, and testing

* Shared Libraries
* Static Libraries
* Executables
* Python Modules
* C++ Modules
* Fortran Modules
* etc

#### Languages

Test all languages supported by Spack

* C/C++
* Fortran
* Python
* Rust
* Go
* R
* Ruby
* Java
* CUDA
* Lua

#### MPI

MPI introduces a lot of Spack logic. With a properly constructed integration test, we can have guarantees of basic MPI related behaviors functioning in Spack and behaving as expected without an expensive or potentiall no-op Gitlab CI run.

##### MPI Challenges

None forseen, Spack can install MPI. We may not be able to get a high rank test running, but that's not really the intent of this repo

#### GPU/CUDA/ROCM

Nvidia packages, ROCM, GPU development, and CUDA all introduce further complication into Spack's logic, this allows us to guarantee stability

##### Cuda Challenges

CUDA is generally available on GHA runners, but GPUs are not. Additional considerations will need to be made to dertermine, how, if at all, we implement CUDA based integration testing as part of this repo.

#### HIP

HIP integration testing could be valuable

##### HIP Challenges

Feasibility to be investigated
