# Spack Smoke/Integration Testing

Tests production context runs of Spack

* Isolates behavior from individual package quirks
* Guaruntees builds without worrying about Gitlab CI's pruning mechanisms (no "nothing to rebuild")
* Directly tests specific Spack behaviors via controlled, deliberatly composed packages relying on specific behaviors
* Production style useage of Spack allows a deliberate testing environment beyond the limited and contrived nature of unit tests
* In the event of failure revealed by the integration tests, allows for much faster development cycles without needing to wait
hours for Gitlab to complete.
* Reduces AWS costs by catching some failures before kicking off expensive Gitlab CI pipelines

## Currently Tested Behavior

Compiler and Package detection

Repo - Adding a repo beyond builtin and utilizing packages from it

Fetching - Fetching a package's source from a local file url

Staging - Successfully staging a packages source

Building - Executing a build system and driving the build of that system

Installing - Installing the package from the build tree

Testing - Validates the software built and installed actually runs

Each of these higher level tasks exercises many more atomic sections of Spack that are well covered by our unit tests.
The purpose served by this test is to validate the integration and compatibility of each of these more atomic components (hence, integration testing :) )

### Roadmap for future Tests

Build systems - Expand beyond CMake

Platforms - Platform specific tests

Architectures - Arch specific tests

Urls - different types of URLs to fetch from

Configs - different config setups

Repos - More complex repo setups

Packages - Packages doing more complex things, packages that depend on each other, virtuals, etc

Libs and executables - test all types

Modules - test usage of modules

#### MPI

MPI introduces a lot Spack logic. With a properly constructed integration test, we can have guarantees
of basic MPI related behaviors functioning in Spack and behaving as expected without an expensive or potentiall no-op Gitlab CI run.

##### Challenges

None forseen, Spack can install MPI. We may not be able to get a high rank test running, but that's not really the intent of this repo

#### GPU/CUDA/ROCM

Nvidia packages, ROCM, GPU development, and CUDA all introduce further complication into Spack's logic, this allows us to guaruntee stability

##### Challenges

CUDA is available on GHA runners, but GPUs are not universally available and may cost money/have a higher overhead. We may need to self host, reach out to Github about pricing options, or simply be incredbly selective about when this check is run

#### HIP

HIP integration testing could be valuable

##### Challenges

Feasabiliity to be investigated\


## FAQ

Coming Soon
