# Spack CI generators

This document describes how the ci module can be extended to provide novel
ci generators.  The module currently has two generators, for gitlab and for
snakemake.  The snakemake generator is provided as a proof-of-concept of the
notion of adding new generators.

The process of generating a pipeline involves creating a ci-enabled spack
environment, activating it, and running `spack ci generate`, possibly with
arguments describing things like where the output should be written.

Internally pipeline generation is broken into two components: general and
ci platform specific.

## General pipeline functionality

General pipeline functionality includes building a pipeline graph (really,
a forest), pruning it in a variety of ways, and gathering attributes for all
the generated spec build jobs from the spack configuration.

All of the above functionality is defined in the `__init__.py` of the top-level
ci module, and should be roughly the same for pipelines generated for any
platform.

## CI platform specific funcionality

Functionality specific to CI platforms (e.g. gitlab, gha, etc.) should be
defined in modules within the `generators` sub-module.  In order to define
a generator for a new platform, there are only a few requirements:

1. add a module under `generators` in which you define a generator method
decorated with the `@generator` attribute.

1. import the new module at the bottom of `ci/generators/__init__.py`, so
that your new generator is automatically registered.

1. the generator method must take as arguments PipelineDag, SpackCI,
PipelineOptions, and PruningResults objects, in that order.

1. the generator method must produce an output file containing the
generated pipeline.

## The snakemake generator

The snakemake generator is provided mainly as an example which users
can experiment with, without needing a large infrastructure set up.

First create a test directory (let's call it `/work/test`, for the purposes
of this document), and put the spack environment you see below inside it.  So
now you should have the following: `/work/test/spackenv/spack.yaml`

```
spack:
  view: false

  config:
    concretizer: clingo
    db_lock_timeout: 120
    install_tree:
      root: /work/test/data/opt
      projections:
        all: '{architecture}/{compiler.name}-{compiler.version}/{name}-{version}-{hash}'

  concretizer:
    reuse: false
    unify: false

  specs:
    - 'uncrustify build_system=autotools'
    - 'uncrustify build_system=cmake'
    - lz4  # MakefilePackage
    - mpich~fortran  # AutotoolsPackage
    - py-setuptools  # PythonPackage
    - openjpeg  # CMakePackage
    - r-rcpp  # RPackage
    - ruby-rake  # RubyPackage

  ci:
    target: snakemake
    pipeline-gen:
    - build-job:
        script::
          - spack env activate --without-view ${SPACK_CONCRETE_ENV_DIR}
          - spack install /${SPACK_JOB_SPEC_DAG_HASH}

  mirrors:
    buildcache-destination:
        fetch: file:///work/test/mirror
        push: file:///work/test/mirror
        source: false
        binary: true

```

Note that the `target` is set to `snakemake`, and that in the `snakemake.py`
module, the generator method is decorated with:

```
@generator("snakemake")
```

This is how `spack ci generate` knows to generate a `Snakefile` from your environment,
rather than, say, a `.gitlab-ci.yml` file.  Next, activate and concretize the environment:

```
spack env activate --without-view /work/test/spackenv
spack concretize
```

Concretizing, above, is optional.  The ci module will do that for you, if it's not done already.
Now you can generate the `Snakefile`:

'''
spack ci generate --artifacts-root data --output-file /work/test/Snakefile
'''

To test the generated `Snakefile`, you need `snakemake` installed.  Spack provides this
package, but you could also install it in a virtual environment with `pip``.  Once it is
installed:

```
snakemake -np --cores <n>
```

The command above will read the `Snakefile` and do a dry run showing how the jobs will be
scheduled and run.  To actually run it:

```
snakemake --latency-wait 21600 --cores 4
```

By default, `snakemake` will only wait 5 seconds for expected output files to appear, so
providing a nice long timeout of 6 hrs will allow even the longest spack packages to build
on even the slowest machines.